import json

from datetime import datetime

from weather_crawler.api import add_ingestion_time


def test_add_ingestion_time():
    inputs = "{}"
    full_date = f"{datetime.now():%Y-%m-%d_%H_%M}"

    result = add_ingestion_time(inputs, full_date)

    assert "ingested_at" in json.loads(result).keys()
    assert json.loads(result)["ingested_at"] == full_date
