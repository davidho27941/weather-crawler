import os
import json
import aiohttp

from fastapi import FastAPI, APIRouter
from datetime import datetime, timedelta

from google.cloud import storage
from google.api_core.exceptions import ClientError

router = APIRouter(prefix="/v1")

TOKEN = os.environ["CWA_AUTH_TOKEN"]


@router.get("/weather", status_code=200)
async def get_weather_data(): ...


@router.get("/weather_station", status_code=200)
async def get_weather_station_info(): ...


@router.get("/rain_fall_station", status_code=200)
async def get_rain_fall_station_data(): ...
