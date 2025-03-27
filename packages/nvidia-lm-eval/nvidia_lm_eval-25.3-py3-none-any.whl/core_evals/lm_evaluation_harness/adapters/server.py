""" Main server holding entry-point to all the interceptors.

The arch is as follows:


         ┌─────────────────────┐
         │                     │
         │  core-eval harness  │
         │                     │
         └───▲──────┬──────────┘
             │      │
     returns │      │
             │      │ calls
             │      │
             │      │
         ┌───┼──────┼──────────────────────────────────────────────────┐
         │   │      ▼                                                  │
         │ AdapterServer (@ localhost:3825)                            │
         │                                                             │
         │   ▲      │       chain of RequestInterceptors:              │
         │   │      │       flask.Request                              │
         │   │      │       is passed on the way up                    │
         │   │      │                                                  │   ┌──────────────────────┐
         │   │ ┌────▼───────────────────────────────────────────────┐  │   │                      │
         │   │ │intcptr_1─────►intcptr_2───►...───►intcptr_N────────┼──┼───►                      │
         │   │ │                     │                              │  │   │                      │
         │   │ └─────────────────────┼──────────────────────────────┘  │   │                      │
         │   │                       │(e.g. for caching interceptors,  │   │  upstream endpoint   │
         │   │                       │ this "shortcut" will happen)    │   │   with actual model  │
         │   │                       │                                 │   │                      │
         │   │                       └─────────────┐                   │   │                      │
         │   │                                     │                   │   │                      │
         │ ┌─┼─────────────────────────────────────▼────┐              │   │                      │
         │ │intcptr'_M◄──intcptr'_2◄──...◄───intcptr'_1 ◄──────────────┼───┤                      │
         │ └────────────────────────────────────────────┘              │   └──────────────────────┘
         │                                                             │
         │              Chain of ResponseInterceptors:                 │
         │              requests.Response is passed on the way down    │
         │                                                             │
         │                                                             │
         └─────────────────────────────────────────────────────────────┘

In other words, interceptors are pieces of independent logic which should be
relatively easy to add separately.



"""

import os

import flask
import requests
import werkzeug.serving

from .adapter_config import AdapterConfig
from .interceptors import (
    AdapterMetadata,
    AdapterRequest,
    AdapterResponse,
    CachingInterceptor,
    EndpointInterceptor,
    NvcfEndpointInterceptor,
    RequestInterceptor,
    ResponseInterceptor,
    ResponseLoggingInterceptor,
    ResponseReasoningInterceptor,
)


class AdapterServer:
    """Main server which serves on a local port and holds chain of interceptors"""

    DEFAULT_ADAPTER_HOST: str = "localhost"
    DEFAULT_ADAPTER_PORT: int = 3825

    adapter_host: str
    adapter_port: int

    request_interceptors: list[RequestInterceptor] = []
    response_interceptors: list[ResponseInterceptor] = []

    app: flask.Flask

    api_url: str

    def __init__(
        self,
        api_url: str,
        adapter_config: AdapterConfig,
    ):
        """
        Initializes the app, creates server and adds interceptors

        Args:
            adapter_config: should be obtained from the main framework config, see `adapter_config.py`
        """
        self.app = flask.Flask(__name__)
        self.app.route("/", defaults={"path": ""}, methods=["POST"])(self._handler)
        self.app.route("/<path:path>", methods=["POST"])(self._handler)

        self.adapter_host: str = os.environ.get(
            "ADAPTER_HOST", self.DEFAULT_ADAPTER_HOST
        )
        self.adapter_port: int = int(
            os.environ.get("ADAPTER_PORT", self.DEFAULT_ADAPTER_PORT)
        )

        self.api_url = api_url

        self._build_interceptor_chains(
            use_request_caching=adapter_config.use_request_caching,
            request_caching_dir=adapter_config.request_caching_dir,
            use_reasoning=adapter_config.use_reasoning,
            end_reasoning_token=adapter_config.end_reasoning_token,
            use_response_logging=adapter_config.use_response_logging,
            use_nvcf=adapter_config.use_nvcf,
        )

    def _build_interceptor_chains(
        self,
        use_request_caching: bool,
        request_caching_dir: str,
        use_reasoning: bool,
        end_reasoning_token: str,
        use_response_logging: bool,
        use_nvcf: bool,
    ):
        cache_interceptor: CachingInterceptor | None = None
        if use_request_caching:
            cache_interceptor = CachingInterceptor(cache_dir=request_caching_dir)
            self.request_interceptors.append(cache_interceptor)
        if use_nvcf:
            self.request_interceptors.append(
                NvcfEndpointInterceptor(api_url=self.api_url)
            )
        else:
            self.request_interceptors.append(EndpointInterceptor(api_url=self.api_url))

        # reverse
        if cache_interceptor:
            self.response_interceptors.append(cache_interceptor)
        if use_response_logging:
            self.response_interceptors.append(ResponseLoggingInterceptor())
        if use_reasoning:
            self.response_interceptors.append(
                ResponseReasoningInterceptor(end_reasoning_token=end_reasoning_token)
            )

    def run(self) -> None:
        """Start the Flask server."""
        werkzeug.serving.run_simple(
            hostname=self.adapter_host,
            port=self.adapter_port,
            application=self.app,
            threaded=True,
        )

    # The headers we don't want to let out
    _EXCLUDED_HEADERS = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]

    @classmethod
    def _process_response_headers(
        cls, response: requests.Response
    ) -> list[tuple[str, str]]:
        """Process response headers, removing excluded ones."""
        return [
            (k, v)
            for k, v in response.headers.items()
            if k.lower() not in cls._EXCLUDED_HEADERS
        ]

    def _handler(self, path: str) -> flask.Response:
        adapter_request = AdapterRequest(
            r=flask.request,
            meta=AdapterMetadata(),
        )
        adapter_response = None
        for interceptor in self.request_interceptors:
            output = interceptor.intercept_request(adapter_request)

            if isinstance(output, AdapterResponse):
                adapter_response = output
                break
            if isinstance(output, AdapterRequest):
                adapter_request = output

        # TODO(agronskiy): asserts in prod are bad, make this more elegant.
        assert adapter_response is not None, "There should be a response to process"
        for interceptor in self.response_interceptors:
            adapter_response = interceptor.intercept_response(adapter_response)

        return flask.Response(
            response=adapter_response.r.content,
            status=adapter_response.r.status_code,
            headers=self._process_response_headers(adapter_response.r),
        )
