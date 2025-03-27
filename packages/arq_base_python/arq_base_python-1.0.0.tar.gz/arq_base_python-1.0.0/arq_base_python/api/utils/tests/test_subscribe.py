import pytest
import asyncio
from reactivex import of
from api.utils.subscribe import auto_subscribe


@auto_subscribe(to_list=True)
def sync_func():
    return of(1, 2, 3)


@auto_subscribe(to_list=True)
async def async_func():
    return of(1, 2, 3)


@auto_subscribe(to_list=False)
def sync_func_no_list():
    return of(1, 2, 3)


@auto_subscribe(to_list=False)
async def async_func_no_list():
    return of(1, 2, 3)


@auto_subscribe()
def non_observable_func():
    return "Not an Observable"


@pytest.mark.asyncio
async def test_auto_subscribe_to_list():
    result = sync_func()
    assert result == [1, 2, 3]


@pytest.mark.asyncio
async def test_auto_subscribe_to_list_async():
    result = await async_func()
    assert result == [1, 2, 3]


@pytest.mark.asyncio
async def test_auto_subscribe_no_list():
    result = sync_func_no_list()
    assert result == 3


@pytest.mark.asyncio
async def test_auto_subscribe_no_list_async():
    result = await async_func_no_list()
    assert result == 3


@pytest.mark.asyncio
async def test_non_observable_func():
    result = non_observable_func()
    assert result == "Not an Observable"
