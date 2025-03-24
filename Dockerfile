FROM python:3.12 AS base

RUN apt -y update && \
    apt -y install vim && \
    pip install uv && \
    mkdir /root/weather-crawler

COPY . /root/weather-crawler
WORKDIR /root/weather-crawler
RUN uv pip install --system -r requirements.txt

ENV GCP_PROJECT_ID=""
ENV WEB_CONCURRENCY=8

EXPOSE 8888

ENTRYPOINT ./entrypoint.sh
