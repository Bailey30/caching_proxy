import requests
import logging
from flask import Flask, jsonify, make_response
from flask.wrappers import Response
from requests.models import CaseInsensitiveDict
from typing import Any

from .cache import Cache


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Server:
    server: Flask
    port: str
    origin: str
    cache: Cache

    def __init__(self, port: str, origin: str, cache: Cache) -> None:
        self.server = Flask(__name__)
        self.port = port
        self.origin = origin
        self.cache = cache

        self.server.add_url_rule(
            "/", view_func=self.handle_request, defaults={"path": ""}
        )
        self.server.add_url_rule(
            "/<path:path>", endpoint="handle_route", view_func=self.handle_request
        )
        # self.sdfgs

    def start(self) -> None:
        self.server.run(port=int(self.port), threaded=True)

    def handle_request(self, path: str) -> Response:
        # First, search for a cached response and handle that.
        cached_response = self.cache.get(path)

        if cached_response:
            return self.response_with_headers(
                cached_response["json"], cached_response["headers"], "HIT"
            )

        # If no cached response, make the api request
        origin_response = requests.get(f"{self.origin}/{path}")

        try:
            json_data = origin_response.json()
            self.cache.put(
                path, {"json": json_data, "headers": origin_response.headers}
            )
            return self.response_with_headers(
                jsonify(json_data), origin_response.headers, "MISS"
            )
        except ValueError:
            logger.warning("Warning: Origin response is not valid JSON.")
            json_data = None
            return self.response_with_headers(
                origin_response.content, origin_response.headers, "MISS"
            )

    def response_with_headers(
        self, data: bytes | Any, headers: CaseInsensitiveDict | dict, cache_header: str
    ) -> Response:
        response = make_response(data)

        # These headers might cause issues if forwarded directly.
        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        ]

        for header, value in headers.items():
            if header.lower() not in excluded_headers:
                response.headers[header] = value

        response.headers["X-Cache"] = cache_header

        print("fdfssdf")

        return response
