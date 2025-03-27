import pytest
import pytest_asyncio
from dataclasses import dataclass
from typing import NamedTuple
from collections.abc import Callable
from uuid import uuid4, UUID

from msgspec import Struct

from kaiju_tools.mapping import convert_struct_type
from kaiju_redis import RedisCache

__all__ = ["TestCache"]


class _Struct(Struct, eq=True):
    key: UUID
    value: bytes
    flag: bool = True


class _CompositeStruct(Struct, eq=True):
    id: int
    obj: _Struct


class _NamedTuple(NamedTuple):
    key: UUID
    value: bytes


@dataclass
class _Class:
    name: str
    value: bool


_StructArray = convert_struct_type(_Struct, array_like=True)
_CompositeStructArray = convert_struct_type(_CompositeStruct, array_like=True)

CACHED_VALUES = {
    "string": lambda: uuid4().hex,
    "number": lambda: uuid4().int % 1024,
    "bytes": lambda: uuid4().bytes,
    "uuid": lambda: uuid4(),
    "dict": lambda: {uuid4().int % 256: uuid4().hex for _ in range(10)},
    "list": lambda: [uuid4().hex for _ in range(10)],
    "set": lambda: {uuid4().hex for _ in range(10)},
    "frozenset": lambda: frozenset({uuid4().hex for _ in range(10)}),
    "tuple": lambda: (uuid4().int % 256, uuid4().hex),
    "namedtuple": lambda: _NamedTuple(key=uuid4(), value=uuid4().bytes),
    "dataclass": lambda: _Class(name=uuid4().hex, value=True),
    "struct": lambda: _Struct(key=uuid4(), value=uuid4().bytes),
    "struct_array": lambda: _StructArray(key=uuid4(), value=uuid4().bytes),
    "composite_struct": lambda: _CompositeStruct(id=uuid4().int % 256, obj=_Struct(key=uuid4(), value=uuid4().bytes)),
    "composite_struct_array": lambda: _CompositeStructArray(
        id=uuid4().int % 256, obj=_Struct(key=uuid4(), value=uuid4().bytes)
    ),
}


@pytest.mark.docker
class TestCache:
    """Test redis cache."""

    @pytest_asyncio.fixture
    async def cache(self, app, redis_cache):
        async with app.services:
            yield redis_cache
            await redis_cache.transport.flushdb()

    async def test_unspecified_type(self, cache: RedisCache):
        key = uuid4().hex
        value = "test"
        await cache.set(key, value, ex=5)
        result = await cache.set(key, value, get=True)
        assert result == value, "previous value must be returned"
        assert await cache.get(key) == result

    @pytest.mark.parametrize("value", CACHED_VALUES.values(), ids=CACHED_VALUES.keys())
    async def test_single_key(self, cache: RedisCache, value: Callable):
        key = uuid4().hex
        value = value()
        await cache.set(key, value, ex=5)
        result = await cache.set(key, value, get=True)
        assert result == value, "previous value must be returned"
        assert await cache.get(key, data_type=type(value)) == result

    @pytest.mark.parametrize("value", CACHED_VALUES.values(), ids=CACHED_VALUES.keys())
    async def test_multi_key(self, cache: RedisCache, value: Callable):
        keys = {uuid4().bytes: value() for _ in range(10)}
        await cache.mset(keys)

        results = await cache.mget(keys, data_type=type(value()))
        assert len(results) == len(keys), "must return the same number of values"
        assert results == list(keys.values()), "all results must match the value"

        num_deleted = await cache.delete(*keys)
        assert num_deleted == len(keys), "number of removed keys must match"
        results = await cache.mget(keys, data_type=type(value()))
        assert len(results) == len(keys), "must return the same number of values"
        assert all(result is None for result in results), "all results must be null values"

    @pytest.mark.parametrize("value", CACHED_VALUES.values(), ids=CACHED_VALUES.keys())
    async def test_hashes(self, cache: RedisCache, value: Callable):
        key = uuid4().bytes
        items = {uuid4().bytes: value() for _ in range(10)}
        num_items = await cache.hset(key, items)
        assert num_items == len(items), "number of added items must match"

        item_key = set(items).pop()
        item = await cache.hget(key, item_key, data_type=type(value()))
        assert item == items[item_key]

        stored_items = await cache.hgetall(key, data_type=type(value()))
        assert stored_items == items

        num_deleted = await cache.hdel(key, *items)
        assert num_deleted == len(items), "number of removed keys must match"
        results = await cache.hgetall(key, data_type=type(value()))
        assert len(results) == 0, "must return nothing"

    @pytest.mark.parametrize("value", CACHED_VALUES.values(), ids=CACHED_VALUES.keys())
    async def test_lists(self, cache: RedisCache, value: Callable):
        key = uuid4().bytes
        items = [value() for _ in range(10)]

        num_items = await cache.rpush(key, *items)
        assert num_items == len(items)

        size = await cache.llen(key)
        assert size == len(items)

        stored_items = await cache.lrange(key, data_type=type(value()))
        assert stored_items == list(items), "not specified range must return all items"

        item = await cache.lpop(key, data_type=type(value()))
        assert item == [items[0]]

        item = await cache.rpop(key, data_type=type(value()))
        assert item == [items[-1]]

        size = await cache.llen(key)
        assert size == len(items) - 2, "must be less by two popped items"
