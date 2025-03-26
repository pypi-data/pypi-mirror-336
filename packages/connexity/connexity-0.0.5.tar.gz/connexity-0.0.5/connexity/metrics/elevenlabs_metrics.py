import json
import time
import logging
from functools import wraps
from math import trunc

from connexity.CONST import CONNEXITY_METRICS_URL
from connexity.utils.send_data import send_data
from fastapi.responses import StreamingResponse
from connexity.metrics.schemas import ElevenlabsRequestBody
from connexity.metrics.utils import contains_full_sentence

logger = logging.getLogger(__name__)


def measure_first_chunk_latency():
    """
    Decorator for FastAPI endpoints that return a StreamingResponse.
    Logs the time to the first sentence (TTFS) from when the endpoint
    function is invoked.
    """
    def actual_decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            start_time = time.time()  # Mark start of endpoint function
            data: ElevenlabsRequestBody = kwargs.get("request_body")
            if data:
                print(data.elevenlabs_extra_body, flush=True)
                sid = data.elevenlabs_extra_body.get("sid")
            else:
                sid = None
            original_response = await method(*args, **kwargs)

            # If the response is not StreamingResponse, just return it
            if not isinstance(original_response, StreamingResponse):
                return original_response

            # Wrap the original response's body_iterator
            async def wrapped_body_iterator():
                first_sentence = True
                sentence = ""
                async for chunk in original_response.body_iterator:
                    try:
                        if first_sentence:
                            data = chunk[5:]
                            data = json.loads(data)
                            sentence += data.get("choices")[0].get("delta").get("content")
                            if contains_full_sentence(sentence):
                                latency = time.time() - start_time
                                print(sentence, flush=True)
                                print(f"[measure_first_chunk_latency] Time to first chunk: {latency:.4f} seconds", flush=True)
                                first_sentence = False
                                data_dict = {"sid": sid,
                                             "latency": trunc(latency * 1000),
                                             "first_sentence": sentence}
                                await send_data(data_dict, api_key='none', url=CONNEXITY_METRICS_URL)
                    except Exception as e:
                        print(f"Exception has occur while processing chunks {e.args}", flush=True)
                    yield chunk

            # Create a new StreamingResponse that uses our wrapped iterator
            new_response = StreamingResponse(
                wrapped_body_iterator(),
                media_type=original_response.media_type
            )

            # Preserve status code and headers from the original response
            new_response.status_code = original_response.status_code
            new_response.headers.update(original_response.headers)

            return new_response

        return wrapper

    return actual_decorator
