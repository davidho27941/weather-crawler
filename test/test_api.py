import pytest

from weather_crawler.api import get_data


@pytest.mark.asyncio
async def test_get_data_invalid_source_type():
    with pytest.raises(ValueError):
        await get_data("endpoint", source_type="unknown")
