import requests
from .cache import Cache
from flask import Flask, request, make_response


class Server:
    def __init__(self, port, origin, cache: Cache):
        self.server = Flask(__name__)
        self.port = port
        self.origin = origin
        self.cache = cache

        self.start()

    def start(self):
        self.server.add_url_rule(
            "/",
            view_func=self.handle_request,
            defaults={"path": ""},
        )
        self.server.add_url_rule(
            "/<path:path>", endpoint="handle_route", view_func=self.handle_request
        )
        self.server.run(port=self.port)

    def handle_request(self, path):
        print(path)
        print("request: ", request)

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

    def response_with_headers(self, data, headers, cache_header):
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
