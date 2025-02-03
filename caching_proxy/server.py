import requests
from flask import Flask, make_response
from flask.wrappers import Response
from requests.models import CaseInsensitiveDict
from typing import Any

from .cache import Cache


class Server:
    def __init__(self, port: int, origin: str, cache: Cache) -> None:
        self.server = Flask(__name__)
        self.port = port
        self.origin = origin
        self.cache = cache

        self.start()

    def start(self) -> None:
        self.server.add_url_rule(
            "/",
            view_func=self.handle_request,
            defaults={"path": ""},
        )
        self.server.add_url_rule(
            "/<path:path>", endpoint="handle_route", view_func=self.handle_request
        )
        self.server.run(port=self.port)

    def handle_request(self, path: str) -> Response:
        cached_response = self.cache.get(path)

        if cached_response:
            return self.response_with_headers(cached_response, {}, "HIT")

        origin_response = requests.get(f"{self.origin}/{path}")

        try:
            json_data = origin_response.json()
        except ValueError:
            print("Warning: Origin response is not valid JSON.")
            json_data = None

        # Optionally cache the JSON response if it's valid
        if json_data is not None:
            self.cache.put(path, json_data)

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

        return response
