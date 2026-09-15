"""Entidades de domínio, montadas a partir das linhas retornadas pelo banco."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


def _timestamp(value: Any) -> str:
    """Normaliza timestamps para ISO 8601: psycopg2 devolve `datetime` para
    colunas TIMESTAMPTZ, enquanto sqlite3 devolve a string já armazenada.
    """
    return value.isoformat() if isinstance(value, datetime) else value


@dataclass
class Technology:
    id: int
    name: str
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: dict) -> "Technology":
        return cls(
            id=int(row["id"]),
            name=row["name"],
            created_at=_timestamp(row["created_at"]),
            updated_at=_timestamp(row["updated_at"]),
        )


@dataclass
class Feedback:
    id: int
    comment: str
    rating: Optional[int]
    project_id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: dict) -> "Feedback":
        return cls(
            id=int(row["id"]),
            comment=row["comment"],
            rating=int(row["rating"]) if row["rating"] is not None else None,
            project_id=int(row["project_id"]),
            created_at=_timestamp(row["created_at"]),
            updated_at=_timestamp(row["updated_at"]),
        )


@dataclass
class Profile:
    id: int
    name: str
    email: str
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: str
    updated_at: str
    projects: list["Project"] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: dict) -> "Profile":
        return cls(
            id=int(row["id"]),
            name=row["name"],
            email=row["email"],
            bio=row["bio"],
            avatar_url=row["avatar_url"],
            created_at=_timestamp(row["created_at"]),
            updated_at=_timestamp(row["updated_at"]),
        )


@dataclass
class Project:
    id: int
    title: str
    description: Optional[str]
    repository_url: str
    profile_id: int
    created_at: str
    updated_at: str
    profile: Optional[Profile] = None
    technologies: list[Technology] = field(default_factory=list)
    feedbacks: list[Feedback] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: dict) -> "Project":
        return cls(
            id=int(row["id"]),
            title=row["title"],
            description=row["description"],
            repository_url=row["repository_url"],
            profile_id=int(row["profile_id"]),
            created_at=_timestamp(row["created_at"]),
            updated_at=_timestamp(row["updated_at"]),
        )
