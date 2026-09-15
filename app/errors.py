"""Tradução das exceções de domínio (e erros de banco) em respostas JSON padronizadas."""

from __future__ import annotations

import sqlite3

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.exceptions import BadRequestException, ConflictException, NotFoundException, ValidationException

try:
    import psycopg2
except ImportError:  # pragma: no cover - ambiente sem driver de Postgres instalado
    psycopg2 = None  # type: ignore[assignment]


def _error_response(status: int, message: str, errors: list[str] | None = None):
    body = {"message": message}
    if errors is not None:
        body["errors"] = errors

    response = jsonify(body)
    response.status_code = status

    return response


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationException)
    def handle_validation_error(exception: ValidationException):
        return _error_response(400, "Erro de validação.", exception.errors)

    @app.errorhandler(NotFoundException)
    def handle_not_found_error(exception: NotFoundException):
        return _error_response(404, str(exception))

    @app.errorhandler(ConflictException)
    def handle_conflict_error(exception: ConflictException):
        return _error_response(409, str(exception))

    @app.errorhandler(BadRequestException)
    def handle_bad_request_error(exception: BadRequestException):
        return _error_response(400, str(exception))

    @app.errorhandler(sqlite3.IntegrityError)
    def handle_sqlite_integrity_error(exception: sqlite3.IntegrityError):
        return _error_response(409, "Violação de restrição de unicidade.")

    if psycopg2 is not None:
        @app.errorhandler(psycopg2.IntegrityError)
        def handle_postgres_integrity_error(exception: "psycopg2.IntegrityError"):
            if getattr(exception, "pgcode", None) == "23505":  # unique_violation
                return _error_response(409, "Violação de restrição de unicidade.")

            return _error_response(500, "Erro interno do servidor.")

    @app.errorhandler(HTTPException)
    def handle_http_exception(exception: HTTPException):
        if exception.code == 404:
            return _error_response(404, "Rota não encontrada.")

        return _error_response(500, "Erro interno do servidor.")

    @app.errorhandler(Exception)
    def handle_unexpected_error(exception: Exception):
        return _error_response(500, "Erro interno do servidor.")
