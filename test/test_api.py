import pytest

from weather_crawler.api import (
    AGRI_RAIN_FALL_URL,
    CWA_WEATHER_URL,
    build_url,
    get_data,
)


@pytest.mark.asyncio
async def test_get_data_invalid_source_type():
    with pytest.raises(ValueError):
        await get_data("endpoint", source_type="unknown")


def test_build_url_invalid_source_type():
    with pytest.raises(ValueError):
        build_url("/api/v1/x", source_type="unknown")


@pytest.mark.parametrize(
    "endpoint",
    ["/api/v1/rest/datastore/O-A0003-001", "api/v1/rest/datastore/O-A0003-001"],
)
def test_build_url_cwa_has_no_empty_path_segment(endpoint):
    url = build_url(endpoint, source_type="cwa")

    assert url.startswith(f"{CWA_WEATHER_URL}/api/v1/rest/datastore/O-A0003-001?")
    assert "//" not in url.removeprefix("https://")
    assert "Authorization=" in url


def test_build_url_agri_uses_agri_host():
    url = build_url("/api/v1/TaiwanRainfallStationInformationType", source_type="agri")

    assert url == f"{AGRI_RAIN_FALL_URL}/api/v1/TaiwanRainfallStationInformationType"
    assert "//" not in url.removeprefix("https://")
    assert "Authorization=" not in url
