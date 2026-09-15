"""Sem endpoints dedicados ainda (ver "Próximas etapas" no README) — mantido
para dar suporte ao relacionamento Project 1:N Feedback já modelado.
"""

from __future__ import annotations

from typing import Optional

from app.entities import Feedback
from app.repositories.abstract_repository import AbstractRepository


class FeedbackRepository(AbstractRepository):
    def find_all_by_project_id(self, project_id: int) -> list[Feedback]:
        rows = self.db.fetchall(
            "SELECT * FROM feedbacks WHERE project_id = ? ORDER BY created_at ASC",
            (project_id,),
        )

        return [Feedback.from_row(row) for row in rows]

    def save(self, comment: str, rating: Optional[int], project_id: int) -> Feedback:
        now = self.now()

        id_ = self.insert(
            "feedbacks",
            ["comment", "rating", "project_id", "created_at", "updated_at"],
            [comment, rating, project_id, now, now],
        )

        row = self.db.fetchone("SELECT * FROM feedbacks WHERE id = ?", (id_,))

        return Feedback.from_row(row)
