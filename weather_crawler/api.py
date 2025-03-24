import os
import json
import aiohttp

from fastapi import FastAPI, APIRouter
from datetime import datetime, timedelta

from google.cloud import storage
from google.api_core.exceptions import ClientError

from typing import Tuple

from .decorators import request_with_restries

router = APIRouter(prefix="/v1")

TOKEN = os.environ["CWA_AUTH_TOKEN"]

CWA_WEATHER_URL = "https://opendata.cwa.gov.tw"
AGRI_RAIN_FALL_URL = "https://data.moa.gov.tw"


@request_with_restries
async def get_data(url: str) -> Tuple[int, str]:

    header = {"Content-Type": "application/json"}

    data = {
        "Authorization": f"{TOKEN}",
        "format": "JSON",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header, data=data) as response:
            status_code = response.status
            response_text = await response.text()

    return status_code, response_text


@router.get("/weather", status_code=200)
async def get_weather_data():

    url = f"{CWA_WEATHER_URL}/api/v1/rest/datastore/O-A0003-001"

    status_code, responce_text = await get_data(url)


@router.get("/weather_station", status_code=200)
async def get_weather_station_info(type: str):

    match type:
        case "manned":
            endpoint = "/api/v1/rest/datastore/C-B0074-001"
        case "unmanned":
            endpoint = "/api/v1/rest/datastore/O-B0074-002"
        case _:
            raise ValueError(f"Provided argument {type} is invalid.")

    url = f"{CWA_WEATHER_URL}/{endpoint}"

    status_code, responce_text = await get_data(url)


@router.get("/rain_fall_station", status_code=200)
async def get_rain_fall_station_data():

    endpoint = "/api/v1/TaiwanRainfallStationInformationType"

    url = f"{AGRI_RAIN_FALL_URL}/{endpoint}"

    status_code, responce_text = await get_data(url)
