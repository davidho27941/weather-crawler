import asyncio
import logging
import functools

logger = logging.getLogger(__name__)


def request_with_restries(func):
    @functools.wraps(func)
    async def retry_wrapper(*args, **kwargs):
        MAX_RETRIES_COUNT = 5
        N_RETRIES = 0

        retry_delay_offset = 0.5

        while N_RETRIES < MAX_RETRIES_COUNT:

            status_code, response_text = await func(*args, **kwargs)

            if status_code == 200:

                logger.info(f"Request succeed without error.")

                break
            else:
                logger.warning(
                    f"Error Occured!\n"
                    f"Status Code: {status_code}\n"
                    f"Response Message: {response_text}.\n"
                    f"Retrying! (number of retries: {N_RETRIES}/{MAX_RETRIES_COUNT})\n"
                    f"Retry after {retry_delay_offset}s\n",
                )

                retry_delay_offset += retry_delay_offset
                N_RETRIES += 1
                await asyncio.sleep(retry_delay_offset)

        else:
            logger.error(
                f"Error Occured!\n"
                f"Request's retries Limit reached.\n"
                f"Status Code: {status_code}\n"
                f"Response Message: {response_text}.\n"
                f"Arguments: {args}\n",
                f"Keyword Arguments: {kwargs}\n",
            )
            raise RuntimeError(f"Retry limit reached!")

        return status_code, response_text

    return retry_wrapper
