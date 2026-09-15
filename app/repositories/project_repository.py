from __future__ import annotations

from typing import Optional, Sequence

from app.entities import Feedback, Profile, Project, Technology
from app.repositories.abstract_repository import AbstractRepository


class ProjectRepository(AbstractRepository):
    def find_by_id(self, id_: int) -> Optional[Project]:
        row = self.db.fetchone("SELECT * FROM projects WHERE id = ?", (id_,))

        return Project.from_row(row) if row is not None else None

    def find_with_details_by_id(self, id_: int) -> Optional[Project]:
        """Busca o projeto já com profile, technologies e feedbacks carregados."""
        project = self.find_by_id(id_)

        return self._hydrate(project) if project is not None else None

    def find_all_order_by_created_at_desc(self) -> list[Project]:
        rows = self.db.fetchall("SELECT * FROM projects ORDER BY created_at DESC")

        return [self._hydrate(Project.from_row(row)) for row in rows]

    def find_all_by_profile_id(self, profile_id: int) -> list[Project]:
        rows = self.db.fetchall(
            "SELECT * FROM projects WHERE profile_id = ? ORDER BY created_at DESC",
            (profile_id,),
        )

        return [self._hydrate(Project.from_row(row)) for row in rows]

    def save(
        self,
        title: str,
        description: Optional[str],
        repository_url: str,
        profile_id: int,
        technology_ids: Sequence[int],
    ) -> Project:
        now = self.now()

        id_ = self.insert(
            "projects",
            ["title", "description", "repository_url", "profile_id", "created_at", "updated_at"],
            [title, description, repository_url, profile_id, now, now],
        )

        for technology_id in technology_ids:
            self.db.execute(
                "INSERT INTO project_technologies (project_id, technology_id) VALUES (?, ?)",
                (id_, technology_id),
            )
            self.db.commit()

        return self.find_with_details_by_id(id_)

    def _hydrate(self, project: Project) -> Project:
        profile_row = self.db.fetchone("SELECT * FROM profiles WHERE id = ?", (project.profile_id,))
        project.profile = Profile.from_row(profile_row) if profile_row is not None else None

        technology_rows = self.db.fetchall(
            """SELECT t.* FROM technologies t
               INNER JOIN project_technologies pt ON pt.technology_id = t.id
               WHERE pt.project_id = ?
               ORDER BY t.name ASC""",
            (project.id,),
        )
        project.technologies = [Technology.from_row(row) for row in technology_rows]

        feedback_rows = self.db.fetchall(
            "SELECT * FROM feedbacks WHERE project_id = ? ORDER BY created_at ASC",
            (project.id,),
        )
        project.feedbacks = [Feedback.from_row(row) for row in feedback_rows]

        return project
