import pytest
from unittest.mock import AsyncMock

from weather_crawler.decorators import request_with_restries


@pytest.mark.asyncio
async def test_request_with_retries_succeeds_after_multiple_failures(monkeypatch):
    func = AsyncMock(side_effect=[(500, "err"), (500, "err"), (200, "ok")])
    wrapped = request_with_restries(func)
    monkeypatch.setattr("weather_crawler.decorators.asyncio.sleep", AsyncMock())

    status, text = await wrapped()

    assert status == 200
    assert text == "ok"
    assert func.await_count == 3


@pytest.mark.asyncio
async def test_request_with_retries_raises_after_limit(monkeypatch):
    func = AsyncMock(return_value=(500, "err"))
    wrapped = request_with_restries(func)
    monkeypatch.setattr("weather_crawler.decorators.asyncio.sleep", AsyncMock())

    with pytest.raises(RuntimeError):
        await wrapped()

    assert func.await_count == 5
