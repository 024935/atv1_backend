"""Cria as tabelas do domínio caso ainda não existam."""

from __future__ import annotations

from app.config.database import Database

_POSTGRES_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS profiles (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(120) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        bio TEXT,
        avatar_url VARCHAR(500),
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS technologies (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL UNIQUE,
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS projects (
        id BIGSERIAL PRIMARY KEY,
        title VARCHAR(150) NOT NULL,
        description TEXT,
        repository_url VARCHAR(500) NOT NULL,
        profile_id BIGINT NOT NULL REFERENCES profiles(id),
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS project_technologies (
        project_id BIGINT NOT NULL REFERENCES projects(id),
        technology_id BIGINT NOT NULL REFERENCES technologies(id),
        PRIMARY KEY (project_id, technology_id)
    )""",
    """CREATE TABLE IF NOT EXISTS feedbacks (
        id BIGSERIAL PRIMARY KEY,
        comment TEXT NOT NULL,
        rating INTEGER,
        project_id BIGINT NOT NULL REFERENCES projects(id),
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL
    )""",
]

_SQLITE_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        bio TEXT,
        avatar_url TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        repository_url TEXT NOT NULL,
        profile_id INTEGER NOT NULL REFERENCES profiles(id),
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS project_technologies (
        project_id INTEGER NOT NULL REFERENCES projects(id),
        technology_id INTEGER NOT NULL REFERENCES technologies(id),
        PRIMARY KEY (project_id, technology_id)
    )""",
    """CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT NOT NULL,
        rating INTEGER,
        project_id INTEGER NOT NULL REFERENCES projects(id),
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
]


class Schema:
    @staticmethod
    def ensure(db: Database) -> None:
        statements = _SQLITE_STATEMENTS if db.driver == "sqlite" else _POSTGRES_STATEMENTS

        for statement in statements:
            db.execute(statement)

        db.commit()
