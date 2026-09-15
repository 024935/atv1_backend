from __future__ import annotations

from typing import Optional, Sequence

from app.entities import Technology
from app.repositories.abstract_repository import AbstractRepository


class TechnologyRepository(AbstractRepository):
    def find_by_name(self, name: str) -> Optional[Technology]:
        row = self.db.fetchone("SELECT * FROM technologies WHERE name = ?", (name,))

        return Technology.from_row(row) if row is not None else None

    def find_by_id(self, id_: int) -> Optional[Technology]:
        row = self.db.fetchone("SELECT * FROM technologies WHERE id = ?", (id_,))

        return Technology.from_row(row) if row is not None else None

    def find_all_by_id_in(self, ids: Sequence[int]) -> list[Technology]:
        if not ids:
            return []

        placeholders = ", ".join(["?"] * len(ids))
        rows = self.db.fetchall(
            f"SELECT * FROM technologies WHERE id IN ({placeholders})",
            tuple(ids),
        )

        return [Technology.from_row(row) for row in rows]

    def find_all_order_by_name(self) -> list[Technology]:
        rows = self.db.fetchall("SELECT * FROM technologies ORDER BY name ASC")

        return [Technology.from_row(row) for row in rows]

    def save(self, name: str) -> Technology:
        now = self.now()

        id_ = self.insert("technologies", ["name", "created_at", "updated_at"], [name, now, now])

        return self.find_by_id(id_)
