import os

from google.cloud import storage

from .logger import get_logger

logger = get_logger(__name__)

GCP_PROJECT = os.environ["GCP_PROJECT_ID"]


def upload_gcs(data: str, bucket_name: str, blob_name: str):

    logger.info(
        "Background task triggered with following arguments:\n"
        f"{bucket_name=}\n"
        f"{blob_name=}\n"
    )

    client = storage.Client(project=GCP_PROJECT)

    bucket = client.bucket(bucket_name)

    blob = bucket.blob(blob_name)

    try:
        blob.upload_from_string(data)
    except Exception:
        logger.exception(
            f"An error occured when uploading data to {bucket_name} with blob name: {blob_name}."
        )
        raise
    else:
        logger.info("Upload task succeed.")
