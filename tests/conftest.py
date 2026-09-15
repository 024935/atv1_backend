"""Cada teste sobe um banco SQLite isolado em memória e exercita a stack
completa de rotas do Flask, via test client.
"""

from __future__ import annotations

import sqlite3

import pytest

from app import create_app
from app.config.database import Database


@pytest.fixture
def client():
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    db = Database("sqlite", connection)
    app = create_app(db)
    app.testing = True

    with app.test_client() as test_client:
        yield test_client
