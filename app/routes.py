"""Registra as rotas REST da API, delegando para as services de cada domínio."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from app.dto.requests import ProfileCreateRequest, ProjectCreateRequest, TechnologyCreateRequest
from app.dto.responses import profile_response, project_response, technology_response
from app.services.profile_service import ProfileService
from app.services.project_service import ProjectService
from app.services.technology_service import TechnologyService


def register_routes(
    app: Flask,
    profile_service: ProfileService,
    technology_service: TechnologyService,
    project_service: ProjectService,
) -> None:
    @app.get("/")
    def ui():
        """Painel HTML simples (app/templates/index.html) para cadastrar
        perfil, tecnologia e projeto via localhost, sem precisar de curl."""
        return render_template("index.html")

    @app.get("/api")
    def root():
        return jsonify({"name": "DevShowcase API", "status": "ok"})

    @app.post("/api/profiles")
    def create_profile():
        body = request.get_json(silent=True) or {}
        create_request = ProfileCreateRequest.from_dict(body)
        profile = profile_service.create(create_request)

        return jsonify(profile_response(profile)), 201

    @app.get("/api/profiles/<int:profile_id>")
    def find_profile(profile_id: int):
        profile = profile_service.find_by_id(profile_id)

        return jsonify(profile_response(profile))

    @app.post("/api/technologies")
    def create_technology():
        body = request.get_json(silent=True) or {}
        create_request = TechnologyCreateRequest.from_dict(body)
        technology = technology_service.create(create_request)

        return jsonify(technology_response(technology)), 201

    @app.get("/api/technologies")
    def find_all_technologies():
        technologies = [technology_response(technology) for technology in technology_service.find_all()]

        return jsonify(technologies)

    @app.post("/api/projects")
    def create_project():
        body = request.get_json(silent=True) or {}
        create_request = ProjectCreateRequest.from_dict(body)
        project = project_service.create(create_request)

        return jsonify(project_response(project)), 201

    @app.get("/api/projects")
    def find_all_projects():
        raw_profile_id = request.args.get("profileId")
        profile_id = int(raw_profile_id) if raw_profile_id not in (None, "") else None

        projects = [project_response(project) for project in project_service.find_all(profile_id)]

        return jsonify(projects)
