from __future__ import annotations

from typing import Optional

from app.entities import Profile, Project
from app.repositories.abstract_repository import AbstractRepository


class ProfileRepository(AbstractRepository):
    def find_by_email(self, email: str) -> Optional[Profile]:
        row = self.db.fetchone("SELECT * FROM profiles WHERE email = ?", (email,))

        return Profile.from_row(row) if row is not None else None

    def find_by_id(self, id_: int) -> Optional[Profile]:
        row = self.db.fetchone("SELECT * FROM profiles WHERE id = ?", (id_,))

        return Profile.from_row(row) if row is not None else None

    def find_with_projects_by_id(self, id_: int) -> Optional[Profile]:
        """Busca o perfil já com a lista de projetos vinculados."""
        profile = self.find_by_id(id_)
        if profile is None:
            return None

        rows = self.db.fetchall(
            "SELECT * FROM projects WHERE profile_id = ? ORDER BY created_at DESC",
            (id_,),
        )
        profile.projects = [Project.from_row(row) for row in rows]

        return profile

    def save(self, name: str, email: str, bio: Optional[str], avatar_url: Optional[str]) -> Profile:
        now = self.now()

        id_ = self.insert(
            "profiles",
            ["name", "email", "bio", "avatar_url", "created_at", "updated_at"],
            [name, email, bio, avatar_url, now, now],
        )

        return self.find_by_id(id_)
