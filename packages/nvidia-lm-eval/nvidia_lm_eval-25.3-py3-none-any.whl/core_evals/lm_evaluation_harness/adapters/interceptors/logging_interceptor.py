import json
from typing import final

import requests
import structlog

from .types import AdapterResponse, ResponseInterceptor


@final
class ResponseLoggingInterceptor(ResponseInterceptor):
    _logger: structlog.BoundLogger

    def __init__(self):
        self._logger = structlog.get_logger(__name__)

    @final
    def intercept_response(self, ar: AdapterResponse) -> AdapterResponse:
        self._logger.info(
            "Logging response", payload=ar.r.json(), cache_hit=ar.meta.cache_hit
        )
        return ar
