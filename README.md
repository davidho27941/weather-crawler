# weather-crawler
A Cloud Run based Crawler for weather data.

## Overview
This FastAPI-based crawler retrieves weather and station data and uploads the
results as JSON files to a Google Cloud Storage (GCS) bucket.

## Prerequisites
- Python 3.12 or newer
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  Core packages include:
  - fastapi==0.115.8
  - pandas==2.2.3
  - pydantic==2.10.6
  - uvicorn==0.34.0
  - aiohttp==3.11.13
  - google-cloud-storage==3.1.0
  - httpx==0.28.1
  - asynctest==0.13.0
  - pytest-asyncio==0.25.3

## Environment Variables
Set the following variables before running the application:
- `CWA_AUTH_TOKEN` – authorization token for weather APIs
- `GCS_BUCKET` – bucket name used to store JSON files
- `GCP_PROJECT_ID` – Google Cloud project containing the bucket

## Usage
Start the service with:
```bash
uvicorn app:app --host 0.0.0.0 --port 8888
```

Available endpoints:
- `GET /v1/weather`
- `GET /v1/weather_station?stn_type=<manned|unmanned>`
- `GET /v1/rain_fall_station`

## Testing
Run tests using:
```bash
pytest
```
