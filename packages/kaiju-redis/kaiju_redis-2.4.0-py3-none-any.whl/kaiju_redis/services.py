"""Redis services."""

import textwrap
from collections.abc import Callable, Collection, Iterable, Mapping
from typing import Any, TypeVar, cast

from coredis import Redis, RedisCluster
from coredis.cache import TrackingCache
from coredis.commands.pubsub import PubSub
from coredis.exceptions import ResponseError, StreamConsumerGroupError
from coredis.pipeline import Pipeline
from msgspec import Struct, convert, msgpack

from kaiju_tools.app import SERVICE_CLASS_REGISTRY, ContextableService
from kaiju_tools.cache import BaseCacheService
from kaiju_tools.encoding import msgpack_dumps, msgpack_loads
from kaiju_tools.functions import retry
from kaiju_tools.locks import BaseLocksService, LockExistsError, NotLockOwnerError
from kaiju_tools.mapping import convert_struct_type
from kaiju_tools.streams import Listener, StreamRPCClient
from kaiju_tools.types import NSKey


__all__ = [
    "RedisTransportService",
    "RedisCacheService",
    "RedisLocksService",
    "RedisListener",
    "RedisStreamRPCClient",
    "RedisSubscriber",
    "RedisPublisher",
    "RedisCache",
]

_Key = TypeVar("_Key", bound=str | bytes)
_CachedItem = TypeVar("_CachedItem", bound=Struct | Any)


class RedisTransportService(ContextableService):
    """Redis transport.

    It provides a service layer for `coredis client <https://coredis.readthedocs.io/en/stable/api/clients.html>`_
    and includes its initialization.
    """

    transport_class = Redis
    cluster_transport_class = RedisCluster

    def __init__(
        self,
        app,
        *args,
        cluster: bool = False,
        tracking: bool = False,
        tracking_cache_settings: dict = None,
        connect_timeout: int = 30,
        max_idle_time: int = 60,
        retry_on_timeout=True,
        logger=None,
        **kws,
    ):
        """Initialize.

        :param app: web app
        :param args: additional transport cls args
        :param cluster: use cluster connector class
        :param tracking: use tracking cache for this connector,
          see `tracking cache <https://coredis.readthedocs.io/en/stable/api/caching.html#coredis.cache.TrackingCache>`_
          Do not use tracking cache for streams / pub-sub queues.
        :param tracking_cache_settings: tracking cache settings for `coredis.cache.TrackingCache`
        :param connect_timeout: connection timeout
        :param max_idle_time: max connection idle time
        :param retry_on_timeout: retry connection on timeout
        :param logger: optional logger instance
        :param kws: additional transport cls args
        """
        super().__init__(app, logger=logger)
        if cluster:
            cls = self.cluster_transport_class
        else:
            cls = self.transport_class
        if tracking:
            tracking_cache_settings = tracking_cache_settings if tracking_cache_settings else {}
            cache = TrackingCache(**tracking_cache_settings)
        else:
            cache = None
        self._transport = cls(
            *args,
            connect_timeout=connect_timeout,
            max_idle_time=max_idle_time,
            retry_on_timeout=retry_on_timeout,
            cache=cache,
            **kws,
        )

    @property
    def transport(self) -> Redis:
        return self._transport

    def __getattr__(self, item):
        return getattr(self._transport, item)

    async def init(self):
        self.connection_pool.reset()

    async def close(self):
        self.connection_pool.disconnect()


class RedisCache(ContextableService):
    """Redis cache service."""

    _transport: Redis

    def __init__(self, *args, transport: RedisTransportService, **kws):
        super().__init__(*args, **kws)
        self._transport_service = transport
        self._encode = msgpack.Encoder(uuid_format="bytes").encode
        self._decode = msgpack.decode
        self._decoders: dict[type, Callable[[bytes], ...]] = {Any: msgpack.decode}
        self._struct_to_array: dict[type[Struct], type[Struct]] = {}  # maps dict-like struct types to array-like

    @property
    def transport(self) -> Redis:
        return self._transport

    async def exists(self, keys: _Key) -> int:
        """Check if keys exist and return their number."""
        return await self._transport.exists(keys)

    async def set(
        self, key: _Key, obj: _CachedItem, *, conn: Pipeline = None, ex: int = None, get: bool = False, **redis_args
    ) -> _CachedItem | None | bool:
        """Set object to the cache.

        :param key: object key
        :param obj: data
        :param conn: optional redis pipe
        :param ex: expiration time in seconds
        :param get: get the previous value (or None if not exists)
        :param redis_args: other arguments for the Redis get method

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            if get=True then the previous value will be returned if present
            otherwise returns `True` if the value has been set successfully
        """
        if conn:
            if isinstance(obj, Struct):
                arr_typ = self.get_struct_array_type(type(obj))
                obj = convert(obj, type=arr_typ, from_attributes=True)
            await conn.set(key, self._encode(obj), ex=ex, get=get, **redis_args)
            return None

        if isinstance(obj, Struct):
            arr_typ = self.get_struct_array_type(type(obj))
            new_obj = convert(obj, type=arr_typ, from_attributes=True)
            result = await self._transport.set(key, self._encode(new_obj), ex=ex, get=get, **redis_args)  # noqa: ???
            if get and result:
                result = cast(bytes, result)
                if type(obj) is type(new_obj):
                    return self._decoders[arr_typ](result)
                return convert(self._decoders[arr_typ](result), type=type(obj), from_attributes=True)
            return None

        result = await self._transport.set(key, self._encode(obj), ex=ex, get=get, **redis_args)  # noqa: ???
        if get and result:
            result = cast(bytes, result)
            return self._decode(result, type=type(obj))

        return None

    async def get(self, key: _Key, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None) -> _CachedItem | None:
        """Get a single item from the cache.

        :param key: cache key
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :returns: item or `None` if not found
        """
        if conn is None:
            conn = self._transport
        result = await conn.get(key)
        if not result:
            return None
        result = cast(bytes, result)
        if data_type and issubclass(data_type, Struct):
            arr_typ = self.get_struct_array_type(data_type)
            obj = self._decoders[arr_typ](result)
            obj = convert(obj, type=data_type, from_attributes=True)
            return obj

        return self._decode(result, type=data_type)

    async def mget(
        self, keys: Collection[_Key], data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> list[_CachedItem | None]:
        """Get multiple items from the cache.

        :param keys: list of cache keys
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :return: a list of cached items, `None` for not found items
        """
        if conn is None:
            conn = self._transport
        result = await conn.mget(keys)
        return self._decode_list_of_values(result, data_type)

    async def delete(self, *keys: _Key, conn: Pipeline = None) -> int | None:
        """Delete one or more keys.

        :param keys: list of keys to delete
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns the number of keys deleted
        """
        if conn is None:
            conn = self._transport
        return await conn.delete(keys)

    async def mset(self, items: Mapping[_Key, _CachedItem], *, conn: Pipeline = None) -> bool | None:
        """Set multiple items to the cache.

        :param items: a mapping from key to item
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns `True` if all was successfully set
        """
        if conn is None:
            conn = self._transport
        data = {}
        for key, item in items.items():
            if isinstance(item, Struct):
                arr_typ = self.get_struct_array_type(type(item))
                item = convert(item, type=arr_typ, from_attributes=True)
            data[key] = self._encode(item)
        return await conn.mset(data)

    async def hset(self, key: _Key, items: Mapping[_Key, _CachedItem], *, conn: Pipeline = None) -> int | None:
        """Set multiple items to the hash key.

        :param key: cache key
        :param items: a mapping from key to item
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns number of items set
        """
        if conn is None:
            conn = self._transport
        data = {}
        for item_key, item in items.items():
            if isinstance(item, Struct):
                arr_typ = self.get_struct_array_type(type(item))
                item = convert(item, type=arr_typ, from_attributes=True)
            data[item_key] = self._encode(item)
        return await conn.hset(key, data)

    async def hget(
        self, key: _Key, item_key: _Key, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> _CachedItem | None:
        """Get a single item from a hash key.

        :param key: hash key
        :param item_key: key inside the hash
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :returns: item or `None` if not found
        """
        if conn is None:
            conn = self._transport
        result = await conn.hget(key, item_key)
        if not result:
            return None
        result = cast(bytes, result)
        if issubclass(data_type, Struct):
            arr_typ = self.get_struct_array_type(data_type)
            obj = self._decoders[arr_typ](result)
            obj = convert(obj, type=data_type, from_attributes=True)
            return obj

        return self._decode(result, type=data_type)

    async def hgetall(
        self, key: _Key, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> dict[bytes, _CachedItem]:
        """Get all values from a hash.

        :param key: hash key
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :returns: item or `None` if not found
        """
        if conn is None:
            conn = self._transport
        result = await conn.hgetall(key)
        if not result:
            return {}
        values = self._decode_list_of_values(result.values(), data_type)
        return dict(zip(result, values))

    async def hdel(self, key: _Key, *item_keys: _Key, conn: Pipeline = None) -> int | None:
        """Delete items from a hash.

        :param key: hash key
        :param item_keys: item keys
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns number of items deleted
        """
        if conn is None:
            conn = self._transport
        return await conn.hdel(key, item_keys)

    async def lpush(self, key: _Key, *items: _CachedItem, conn: Pipeline = None) -> int | None:
        """Set multiple items to the list.

        :param key: cache key
        :param items: collection of items
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns the length of the list after the push operations
        """
        if conn is None:
            conn = self._transport
        data = []
        for item in items:
            if isinstance(item, Struct):
                arr_typ = self.get_struct_array_type(type(item))
                item = convert(item, type=arr_typ, from_attributes=True)
            data.append(self._encode(item))
        return await conn.lpush(key, data)

    async def rpush(self, key: _Key, *items: _CachedItem, conn: Pipeline = None) -> int | None:
        """Set multiple items to the list.

        :param key: cache key
        :param items: collection of items
        :param conn: optional redis pipe

        :return: if conn is provided then nothing is returned (user must handle returns manually)
            otherwise returns the length of the list after the push operations
        """
        if conn is None:
            conn = self._transport
        data = []
        for item in items:
            if isinstance(item, Struct):
                arr_typ = self.get_struct_array_type(type(item))
                item = convert(item, type=arr_typ, from_attributes=True)
            data.append(self._encode(item))
        return await conn.rpush(key, data)

    async def lrange(
        self, key: _Key, start: int = 0, stop: int = -1, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> list[_CachedItem | None]:
        """Get multiple items from the list.

        :param key: list key
        :param start: first index
        :param stop: last index
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :return: a list of cached items
        """
        if conn is None:
            conn = self._transport
        result = await conn.lrange(key, start, stop)
        if not result:
            return []
        return self._decode_list_of_values(result, data_type=data_type)

    async def lpop(
        self, key: _Key, num: int = 1, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> list[_CachedItem]:
        """Pop multiple items from the list.

        :param key: list key
        :param num: number of items
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :return: a list of cached items
        """
        if conn is None:
            conn = self._transport
        result = await conn.lpop(key, num)
        if not result:
            return []
        return self._decode_list_of_values(result, data_type)

    async def rpop(
        self, key: _Key, num: int = 1, data_type: type[_CachedItem] = Any, *, conn: Pipeline = None
    ) -> list[_CachedItem]:
        """Pop multiple items from the list.

        :param key: list key
        :param num: number of items
        :param data_type: item data type to convert to
        :param conn: optional redis pipe

        :return: a list of cached items
        """
        if conn is None:
            conn = self._transport
        result = await conn.rpop(key, num)
        if not result:
            return []
        return self._decode_list_of_values(result, data_type)

    async def llen(self, key: _Key, conn: Pipeline = None) -> int:
        """Get the length of a list."""
        if conn is None:
            conn = self._transport
        return await conn.llen(key)

    def _decode_list_of_values(self, values: Iterable[bytes | None], data_type: type) -> list:
        data = []
        if data_type and issubclass(data_type, Struct):
            array_type = self._struct_to_array[data_type]
            for value in values:
                if not value:
                    data.append(value)
                    continue

                value = self._decoders[array_type](value)
                value = convert(value, type=data_type, from_attributes=True)
                data.append(value)

        else:
            for value in values:
                if not value:
                    data.append(value)
                    continue

                value = self._decode(value, type=data_type)
                data.append(value)

        return data

    def get_struct_array_type(self, struct_type: type[Struct], /) -> type[Struct]:
        """Register a struct type and return its array-like type."""
        if struct_type.__struct_config__.array_like:
            self._struct_to_array[struct_type] = struct_type
            self._decoders[struct_type] = msgpack.Decoder(type=struct_type).decode
            return struct_type
        elif struct_type in self._struct_to_array:
            return self._struct_to_array[struct_type]
        else:
            self._struct_to_array[struct_type] = array_type = convert_struct_type(
                struct_type, array_like=True, omit_defaults=True, recursive=True
            )
            self._decoders[array_type] = msgpack.Decoder(type=array_type).decode
            return array_type

    async def init(self) -> None:
        self._transport_service = self.discover_service(self._transport_service, cls=RedisTransportService)
        self._transport = self._transport_service.transport


class RedisCacheService(BaseCacheService):
    """Redis cache service (legacy).

    .. deprecated:: 2.4

        Use of `RedisCache` recommended.

    """

    _M_SET_EXP_SCRIPT = """
    local ttl = ARGV[1]
    for i, key in pairs(KEYS) do
        redis.call('SETEX', key, ttl, ARGV[i + 1])
    end
    """

    MEXISTS_SCRIPT = """
    local result = {}
    for i, key in pairs(KEYS) do
        result[i] = redis.call('EXISTS', key)
    end
    return result
    """

    _m_set_exp_script = None  #: compiled script
    _m_exists_script = None  #: compiled script
    _transport: RedisTransportService

    async def init(self):
        await super().init()
        self._m_set_exp_script = self._transport.register_script(textwrap.dedent(self._M_SET_EXP_SCRIPT))
        self._m_exists_script = self._transport.register_script(textwrap.dedent(self.MEXISTS_SCRIPT))

    @classmethod
    def get_transport_cls(cls):
        return RedisTransportService

    async def exists(self, id: NSKey) -> bool:
        existing = await self._transport.exists([id])
        return bool(existing)

    async def m_exists(self, id: Collection[NSKey]) -> frozenset[str]:
        keys = await self._m_exists_script.execute(keys=id)
        return frozenset(key for key, value in zip(id, keys) if bool(value))

    async def _get(self, key: str):
        return await self._transport.get(key)

    async def _m_get(self, *keys: str):
        return await self._transport.mget(keys)

    async def _set(self, key: str, value, ttl: int):
        if ttl:
            return await self._transport.setex(key, value, ttl)
        return await self._transport.set(key, value)

    async def _m_set(self, keys: dict, ttl: int):
        if ttl:
            return await self._m_set_exp_script.execute(keys=list(keys.keys()), args=[ttl, *list(keys.values())])
        return await self._transport.mset(keys)

    async def _delete(self, key: str):
        return await self._transport.delete([key])

    async def _m_delete(self, *keys: str):
        self.logger.info("DELETE")
        try:
            await self._transport.delete(keys)
        except Exception as exc:
            self.logger.info(str(exc), exc_info=exc)
        self.logger.info("OK")

    async def lpush(
        self,
        key: NSKey,
        *values,
    ) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        """
        self.logger.info('Add key "%s"', key)
        values = [self._dump_value(v) for v in values]
        await self._transport.lpush(key, values)

    async def rpush(self, key: NSKey, *values) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        """
        self.logger.info('Add key "%s"', key)
        values = [self._dump_value(v) for v in values]
        await self._transport.rpush(key, values)

    async def llen(self, key: NSKey) -> int:
        """Get count of list.

        :param key: string only
        """
        self.logger.info('Get key count "%s"', key)
        return await self._transport.llen(key)

    async def lrange(self, key: NSKey, start=0, end=10):
        """Get values from list by key.

        :param key: string only
        :param start: positive int only
        :param end: positive int only
        """
        self.logger.info("Set range for key %s .", key)
        values = await self._transport.lrange(key, start=start, stop=end)
        if values:
            values = [self._load_value(v) for v in values]
        return values

    async def lpop(self, key: NSKey):
        """Get values from list by key.

        :param key: string only
        """
        self.logger.info("Set range for key %s .", key)
        value = await self._transport.lpop(key)
        if value:
            value = self._load_value(value)
        return value


class RedisLocksService(BaseLocksService):
    """Locks service with Redis backend."""

    class ErrorCode:
        """Error codes used by redis scripts."""

        OK = "OK"
        LOCK_EXISTS = "LOCK_EXISTS"
        NOT_LOCK_OWNER = "NOT_LOCK_OWNER"
        RUNTIME_ERROR = "RUNTIME_ERROR"

    RENEW_SCRIPT = """
    for i, key in pairs(KEYS) do
        redis.call('expire', key, ARGV[i])
    end
    """

    EXISTS_SCRIPT = RedisCacheService.MEXISTS_SCRIPT
    _lock_script = None
    _unlock_script = None
    _renew_script = None
    _exists_script = None
    _transport: RedisTransportService

    async def init(self):
        await super().init()
        self._renew_script = self._transport.register_script(textwrap.dedent(self.RENEW_SCRIPT))
        self._exists_script = self._transport.register_script(textwrap.dedent(self.EXISTS_SCRIPT))

    @classmethod
    def get_transport_cls(cls) -> type:
        return RedisTransportService

    async def m_exists(self, id: list[NSKey]) -> frozenset[NSKey]:
        data = await self._exists_script.execute(keys=id)
        if data:
            return frozenset(key for key, value in zip(id, data) if bool(value))
        return frozenset()

    async def _acquire(self, keys: list, identifier: str, ttl: int):
        for key in keys:
            result = await self._transport.set(str(key), str(identifier), condition="NX", ex=ttl)
            if not result:
                raise LockExistsError(self.ErrorCode.LOCK_EXISTS)

    async def _release(self, keys: list, identifier: str):
        for key in keys:
            identifier = identifier.encode("utf-8")
            key_id = await self._transport.get(key)
            if key_id != identifier:
                raise NotLockOwnerError(self.ErrorCode.NOT_LOCK_OWNER)
            await self._transport.delete([key])

    async def _renew(self, keys: list, values: list):
        await self._renew_script.execute(keys=keys, args=[int(v) for v in values])

    async def _owner(self, key: str):
        owner = await self._transport.get(key)
        if owner:
            owner = owner.decode("utf-8")
            return owner


class RedisListener(Listener):
    """Redis stream listener."""

    _transport: RedisTransportService
    _loads = msgpack_loads
    _trim_interval = 300  # s
    _trim_op = b"~"

    def __init__(
        self,
        *args,
        group_id: str = None,
        consumer_id: str = None,
        max_batch_size: int = 10,
        max_wait_time_ms: int = 500,
        pending_messages_time_ms: int = None,
        trim_size: int = 10_000_000,
        trim_delivered: bool = True,
        **kws,
    ):
        """Initialize.

        :param args: listener args
        :params kws: listener kws
        :param group_id: consumer group, `app.name` by default
        :param consumer_id: unique instance id, `app.id` by default
        :param max_batch_size: max single acquired batch size
        :param max_wait_time_ms: max wait time when waiting for a batch
        :param pending_messages_time_ms: processing pending messages timeout in ms
            (messages not acked since this interval will be auto-claimed by this listener)
            set `None` to disable this behavior
        :param trim_delivered: trim all delivered messages
        :param trim_size: stream records trim size: older records will be removed
            if the stream is longer than this value
            set `None` to disable this behavior
            note that this function is disabled if `trim_delivered` is set
        """
        super().__init__(*args, **kws)
        self.group_id = group_id if group_id else self.app.name
        self.consumer_id = consumer_id if consumer_id else str(self.app.id)
        self.max_batch_size = max_batch_size
        self.max_wait_time_ms = max_wait_time_ms
        self.pending_messages_time_ms = pending_messages_time_ms
        self.trim_size = trim_size
        self.trim_delivered = trim_delivered
        self._task_claim_pending = None
        self._task_trim_records = None

    async def init(self):
        await super().init()
        await self._create_group()
        if self.pending_messages_time_ms:
            interval = max(1, self.pending_messages_time_ms // 1000)
            self._task_claim_pending = self._scheduler.schedule_task(
                self._claim_pending, interval=interval, name=f"{self.service_name}._claim_pending"
            )
        if self.trim_delivered:
            self._task_trim_records = self._scheduler.schedule_task(
                self._trim_delivered, interval=self._trim_interval, name=f"{self.service_name}._trim_delivered"
            )
        elif self.trim_size:
            self._task_trim_records = self._scheduler.schedule_task(
                self._trim_records, interval=self._trim_interval, name=f"{self.service_name}._trim_records"
            )

    async def close(self):
        if self._task_claim_pending:
            self._task_claim_pending.enabled = False
        if self._task_trim_records:
            self._task_trim_records.enabled = False
        await super().close()

    async def _create_group(self) -> None:
        self.logger.info("Creating group %s for stream %s", self.group_id, self._key)
        try:
            groups = await self._transport.xinfo_groups(self._key)
            self.logger.debug("groups: %s", groups)
        except ResponseError:
            groups, mk_stream = frozenset(), True
        else:
            groups, mk_stream = frozenset(group[b"name"].decode() for group in groups), False
        if self.group_id not in groups:
            result = await self._transport.xgroup_create(self._key, self.group_id, identifier="$", mkstream=mk_stream)
            self.logger.debug("group create: %s", result)

    def get_transport(self):
        return self.discover_service(self._transport, cls=RedisTransportService)

    async def _read_batch(self) -> list | None:
        try:
            batch = await self._transport.xreadgroup(
                self.group_id,
                self.consumer_id,
                count=self.max_batch_size,
                block=self.max_wait_time_ms,
                streams={self._key: ">"},
                noack=True,
            )
        except StreamConsumerGroupError:
            await self._create_group()
        else:
            if batch:
                batch = next(iter(batch.values()), None)  # first topic, there should only be a single topic
                return batch

    async def _claim_pending(self) -> None:
        """Claim pending messages."""
        await self._transport.xautoclaim(
            self._key, self.group_id, self.consumer_id, self.pending_messages_time_ms, justid=True
        )

    async def _trim_records(self) -> None:
        """Trim older records."""
        result = await self._transport.xtrim(
            self._key, trim_strategy=b"MAXLEN", threshold=self.trim_size, trim_operator=self._trim_op
        )
        self.logger.debug("trim: %s", result)

    async def _trim_delivered(self) -> None:
        """Trim delivered records."""
        groups = await self._transport.xinfo_groups(self._key)
        group = groups[0]
        result = await self._transport.xtrim(self._key, trim_strategy=b"MINID", threshold=group[b"last_delivered"])
        self.logger.debug("trim: %s", result)

    async def _process_batch(self, batch: list) -> None:
        acks = []
        for row in batch:
            row_id, data = row
            data = self._loads(data[b"_"])
            await self._process_request(data)
            acks.append(row_id)
        if acks:
            await retry(
                self._transport.xack,
                args=(self._key, self.group_id),
                kws={"identifiers": acks},
                retries=5,
                retry_timeout=1.0,
                max_retry_timeout=10,
                logger=self.logger,
            )


class RedisStreamRPCClient(StreamRPCClient):
    """Redis stream client."""

    _transport: RedisTransportService
    _dumps = msgpack_dumps

    def get_transport(self):
        return self.discover_service(self._transport, cls=RedisTransportService)

    async def write(self, topic: NSKey, body, headers: dict = None, key=None) -> None:
        """Write data to the stream.

        :param topic: topic key
        :param body: rpc request body
        :param headers: request headers
        :param key: (optional) message id
        """
        await self._transport.xadd(topic, {b"_": self._dumps((body, headers))}, identifier=key if key else "*")


class RedisSubscriber(Listener):
    """Redis PUB/SUB subscriber."""

    _transport: RedisTransportService
    _sub: PubSub = None
    _loads = msgpack_loads
    namespace_prefix = "_sub"

    async def init(self):
        await super().init()
        self._sub = self._transport.pubsub()
        await self._sub.subscribe(self._key)

    async def close(self):
        self._sub.reset()
        self._sub.close()

    def get_transport(self):
        return self.discover_service(self._transport, cls=RedisTransportService)

    async def _read_batch(self) -> list | None:
        message = await self._sub.get_message(ignore_subscribe_messages=True, timeout=None)
        if message is None:
            return []
        return [message]

    async def _process_batch(self, batch: list) -> None:
        for message in batch:
            message = self._loads(message["data"])
            await self._process_request(message)


class RedisPublisher(RedisStreamRPCClient):
    """Redis PUB/SUB publisher."""

    namespace_prefix = RedisSubscriber.namespace_prefix

    async def write(self, topic: NSKey, body, headers: dict = None, key=None) -> None:
        """Write data to the stream.

        :param topic: topic key
        :param body: rpc request body
        :param headers: request headers
        :param key: (optional) message id
        """
        await self._transport.publish(topic, self._dumps((body, headers)))


SERVICE_CLASS_REGISTRY.register(RedisTransportService)
SERVICE_CLASS_REGISTRY.register(RedisCacheService)
SERVICE_CLASS_REGISTRY.register(RedisLocksService)
SERVICE_CLASS_REGISTRY.register(RedisListener)
SERVICE_CLASS_REGISTRY.register(RedisStreamRPCClient)
SERVICE_CLASS_REGISTRY.register(RedisSubscriber)
SERVICE_CLASS_REGISTRY.register(RedisPublisher)
