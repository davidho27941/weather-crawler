import json
import logging
import asyncio

from fastapi import FastAPI, Request

from weather_crawler.logger import get_logger
from weather_crawler.api import router

logger = get_logger(__name__)

app = FastAPI(debug=True)
app.include_router(router)
