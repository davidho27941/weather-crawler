import os
import json
import aiohttp

from fastapi import FastAPI, APIRouter, BackgroundTasks
from datetime import datetime, timedelta

from typing import Tuple

from .logger import get_logger
from .decorators import request_with_restries
from .backgroud_task import upload_gcs


logger = get_logger(__name__)

router = APIRouter(prefix="/v1")

TOKEN = os.environ["CWA_AUTH_TOKEN"]
GCS_BUCKET = os.environ["GCS_BUCKET"]

CWA_WEATHER_URL = "https://opendata.cwa.gov.tw"
AGRI_RAIN_FALL_URL = "https://data.moa.gov.tw"


def add_ingestion_time(data: str, full_date: str) -> str:

    data = json.loads(data)
    data = data | {"ingested_at": full_date}

    return json.dumps(data)


@request_with_restries
async def get_data(endpoint: str, source_type: str = "cwa") -> Tuple[int, str]:

    header = {"Content-Type": "application/json"}

    logger.info(f"Starting to fetch data from {url}.")

    match source_type:
        case "cwa":
            url = f"{CWA_WEATHER_URL}/{endpoint}?Authorization={TOKEN}"

        case "agri":
            url = f"{CWA_WEATHER_URL}/{endpoint}"

        case _:
            raise ValueError("Provided source type not available.")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            status_code = response.status
            response_text = await response.text()

    logger.info("Finished.")

    return status_code, response_text


@router.get("/weather", status_code=200)
async def get_weather_data(background_tasks: BackgroundTasks):

    logger.info("`weather` endpoint has been triggered.")

    endpoint = f"/api/v1/rest/datastore/O-A0003-001"

    status_code, responce_text = await get_data(endpoint)

    date = f"{datetime.now():%Y-%m-%d}"
    date_hhmm = f"{datetime.now():%H_%M}"
    full_date = f"{datetime.now():%Y-%m-%d_%H_%M}"

    data = add_ingestion_time(responce_text, full_date)

    blob_name = f"weather_data/{date}/{date_hhmm}.json"

    background_tasks.add_task(upload_gcs, data, GCS_BUCKET, blob_name)

    logger.info("Request complete.")


@router.get("/weather_station", status_code=200)
async def get_weather_station_info(stn_type: str, background_tasks: BackgroundTasks):

    logger.info(f"`weather_station` endpoint has been triggered with {stn_type} type.")

    match stn_type:
        case "manned":
            endpoint = "/api/v1/rest/datastore/C-B0074-001"
        case "unmanned":
            endpoint = "/api/v1/rest/datastore/C-B0074-002"
        case _:
            raise ValueError(f"Provided argument {stn_type} is invalid.")

    status_code, responce_text = await get_data(endpoint)

    date = f"{datetime.now():%Y-%m-%d}"
    date_hhmm = f"{datetime.now():%H_%M}"
    full_date = f"{datetime.now():%Y-%m-%d_%H_%M}"

    data = add_ingestion_time(responce_text, full_date)

    blob_name = f"weather_station/{stn_type}/{date}/{date_hhmm}.json"

    background_tasks.add_task(upload_gcs, data, GCS_BUCKET, blob_name)

    logger.info("Request complete.")


@router.get("/rain_fall_station", status_code=200)
async def get_rain_fall_station_data(background_tasks: BackgroundTasks):

    logger.info(f"`rain_fall_station` endpoint has been triggered.")

    endpoint = "/api/v1/TaiwanRainfallStationInformationType"

    status_code, responce_text = await get_data(endpoint, source_type="agri")

    date = f"{datetime.now():%Y-%m-%d}"
    date_hhmm = f"{datetime.now():%H_%M}"
    full_date = f"{datetime.now():%Y-%m-%d_%H_%M}"

    data = add_ingestion_time(responce_text, full_date)

    blob_name = f"rain_fall/{date}/{date_hhmm}.json"

    background_tasks.add_task(upload_gcs, data, GCS_BUCKET, blob_name)

    logger.info("Request complete.")
