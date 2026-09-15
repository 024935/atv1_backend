"""Monta a aplicação Flask (rotas, middlewares e tratamento de erros) sem
chamar `app.run()`, permitindo reaproveitar a mesma montagem tanto no
entrypoint (run.py) quanto nos testes automatizados (pytest).
"""

from __future__ import annotations

from flask import Flask

from app.config.database import Database
from app.config.schema import Schema
from app.errors import register_error_handlers
from app.middleware.cors import register_cors
from app.repositories.profile_repository import ProfileRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.technology_repository import TechnologyRepository
from app.routes import register_routes
from app.services.profile_service import ProfileService
from app.services.project_service import ProjectService
from app.services.technology_service import TechnologyService


def create_app(db: Database) -> Flask:
    Schema.ensure(db)

    profile_repository = ProfileRepository(db)
    project_repository = ProjectRepository(db)
    technology_repository = TechnologyRepository(db)

    profile_service = ProfileService(profile_repository)
    technology_service = TechnologyService(technology_repository)
    project_service = ProjectService(project_repository, profile_repository, technology_repository)

    app = Flask(__name__)
    app.json.ensure_ascii = False

    register_cors(app)
    register_routes(app, profile_service, technology_service, project_service)
    register_error_handlers(app)

    return app
