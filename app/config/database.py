"""Conexão com o banco de dados (pgsql ou sqlite), sem ORM (SQL puro)."""

from __future__ import annotations

import os
import sqlite3
from typing import Any, Optional, Sequence

try:  # psycopg2 só é necessário para rodar contra PostgreSQL.
    import psycopg2
    import psycopg2.extras
except ImportError:  # pragma: no cover - ambiente sem driver de Postgres instalado
    psycopg2 = None  # type: ignore[assignment]


class Database:
    """Encapsula a conexão ativa e normaliza o dialeto SQL (`?` -> `%s`)."""

    _connection: Optional["Database"] = None

    def __init__(self, driver: str, connection: Any) -> None:
        self.driver = driver
        self.connection = connection

    @classmethod
    def connection(cls) -> "Database":
        if cls._connection is None:
            cls._connection = cls._create_connection()

        return cls._connection

    @classmethod
    def set_connection(cls, database: "Database") -> None:
        """Permite injetar uma conexão diferente (ex.: SQLite em memória nos testes)."""
        cls._connection = database

    @classmethod
    def _create_connection(cls) -> "Database":
        driver = cls._env("DB_DRIVER", "pgsql")

        if driver == "sqlite":
            path = cls._env("DB_DATABASE", ":memory:")
            connection = sqlite3.connect(path, check_same_thread=False)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")

            return cls("sqlite", connection)

        if psycopg2 is None:  # pragma: no cover
            raise RuntimeError("psycopg2 não está instalado; instale as dependências do projeto.")

        host = cls._env("DB_HOST", "localhost")
        port = cls._env("DB_PORT", "5434")
        database = cls._env("DB_DATABASE", "devshowcase")
        username = cls._env("DB_USERNAME", "postgres")
        password = cls._env("DB_PASSWORD", "postgres")

        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=username,
            password=password,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        connection.autocommit = True

        return cls("pgsql", connection)

    @staticmethod
    def _env(name: str, default: str) -> str:
        value = os.environ.get(name)

        return value if value else default

    def _translate(self, sql: str) -> str:
        return sql if self.driver == "sqlite" else sql.replace("?", "%s")

    def execute(self, sql: str, params: Sequence[Any] = ()):
        cursor = self.connection.cursor()
        cursor.execute(self._translate(sql), tuple(params))

        return cursor

    def fetchone(self, sql: str, params: Sequence[Any] = ()) -> Optional[dict]:
        cursor = self.execute(sql, params)
        row = cursor.fetchone()

        return dict(row) if row is not None else None

    def fetchall(self, sql: str, params: Sequence[Any] = ()) -> list[dict]:
        cursor = self.execute(sql, params)

        return [dict(row) for row in cursor.fetchall()]

    def commit(self) -> None:
        self.connection.commit()
