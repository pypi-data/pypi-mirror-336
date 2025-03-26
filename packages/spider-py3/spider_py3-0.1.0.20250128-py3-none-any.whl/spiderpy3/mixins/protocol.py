import httpx
import requests
from typing import Union

from spiderpy3.utils.logger import Logger


class ProtocolMixin(object):
    logger: Logger

    def logger_debug_response(
            self,
            response: Union[requests.models.Response, httpx.Response],
            response_text_max_length: int = 100,
            response_text_fill_words: str = "..."
    ) -> None:
        text = ""

        if isinstance(response, requests.models.Response):
            text += f"{response.request.method} {response.request.url}\n"

            response_text = response.text
            max_length = response_text_max_length - len(response_text_fill_words)
            if len(response_text) > max_length:
                text += response_text[:max_length] + response_text_fill_words
            else:
                text += response_text

        elif isinstance(response, httpx.Response):
            text += f"{response.request.method} {response.request.url}\n"

            response_text = response.text
            max_length = response_text_max_length - len(response_text_fill_words)
            if len(response_text) > max_length:
                text += response_text[:max_length] + response_text_fill_words
            else:
                text += response_text

        self.logger.debug(text)
