"""Libera `/api/**` para qualquer origem, com os métodos e cabeçalhos usados pela API."""

from __future__ import annotations

from flask import Flask, Response, request


def register_cors(app: Flask) -> None:
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return Response(status=200)

        return None

    @app.after_request
    def add_cors_headers(response: Response) -> Response:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"

        return response
