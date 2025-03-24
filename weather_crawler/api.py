import os
import json
import aiohttp

from fastapi import FastAPI, APIRouter
from datetime import datetime, timedelta

from google.cloud import storage
from google.api_core.exceptions import ClientError

from .decorators import request_with_restries

router = APIRouter(prefix="/v1")

TOKEN = os.environ["CWA_AUTH_TOKEN"]


@request_with_restries
async def get_data(url: str):

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
async def get_weather_data(): ...


@router.get("/weather_station", status_code=200)
async def get_weather_station_info(): ...


@router.get("/rain_fall_station", status_code=200)
async def get_rain_fall_station_data(): ...
