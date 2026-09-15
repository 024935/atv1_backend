"""Base para os repositórios: insere registros e retorna o id gerado, de forma
compatível tanto com PostgreSQL (via `RETURNING id`) quanto com SQLite (via
`lastrowid`), usado nos testes automatizados.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence

from app.config.database import Database


class AbstractRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def insert(self, table: str, columns: Sequence[str], values: Sequence[Any]) -> int:
        column_list = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        sql = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"

        if self.db.driver == "pgsql":
            cursor = self.db.execute(f"{sql} RETURNING id", values)
            row = cursor.fetchone()
            self.db.commit()

            return int(row["id"])

        cursor = self.db.execute(sql, values)
        self.db.commit()

        return int(cursor.lastrowid)

    @staticmethod
    def now() -> str:
        moment = datetime.now(timezone.utc)

        return moment.strftime("%Y-%m-%dT%H:%M:%S.") + f"{moment.microsecond // 1000:03d}Z"
