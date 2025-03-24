from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/v1")


@router.get("/weather", status_code=200)
async def get_weather_data(): ...


@router.get("/weather_station", status_code=200)
async def get_weather_station_info(): ...


@router.get("/rain_fall_station", status_code=200)
async def get_rain_fall_station_data(): ...
