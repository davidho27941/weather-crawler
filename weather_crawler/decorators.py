import asyncio
import functools

from .logger import get_logger

logger = get_logger(__name__)


def request_with_restries(func):
    @functools.wraps(func)
    async def retry_wrapper(*args, **kwargs):
        MAX_RETRIES_COUNT = 5
        N_RETRIES = 0

        retry_delay_offset = 0.5

        while N_RETRIES < MAX_RETRIES_COUNT:

            status_code, response_text = await func(*args, **kwargs)

            if status_code == 200:

                logger.info("Request succeed without error.")

                break
            else:
                logger.warning(
                    "\n".join(
                        [
                            "Error Occured!",
                            f"Status Code: {status_code}",
                            f"Response Message: {response_text}.",
                            f"Retrying! (number of retries: {N_RETRIES}/{MAX_RETRIES_COUNT})",
                            f"Retry after {retry_delay_offset}s",
                        ]
                    )
                )

                retry_delay_offset += retry_delay_offset
                N_RETRIES += 1
                await asyncio.sleep(retry_delay_offset)

        else:
            logger.error(
                "\n".join(
                    [
                        "Error Occured!",
                        "Request's retries Limit reached.",
                        f"Status Code: {status_code}",
                        f"Response Message: {response_text}.",
                        f"Arguments: {args}",
                        f"Keyword Arguments: {kwargs}",
                    ]
                )
            )
            raise RuntimeError(f"Retry limit reached!")

        return status_code, response_text

    return retry_wrapper
