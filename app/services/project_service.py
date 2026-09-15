from __future__ import annotations

from typing import Optional

from app.dto.requests import ProjectCreateRequest
from app.entities import Project
from app.exceptions import BadRequestException, NotFoundException
from app.repositories.profile_repository import ProfileRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.technology_repository import TechnologyRepository


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        profile_repository: ProfileRepository,
        technology_repository: TechnologyRepository,
    ) -> None:
        self.project_repository = project_repository
        self.profile_repository = profile_repository
        self.technology_repository = technology_repository

    def create(self, request: ProjectCreateRequest) -> Project:
        profile_id = request.profile_id()

        if self.profile_repository.find_by_id(profile_id) is None:
            raise BadRequestException(f"Profile com id {profile_id} não encontrado.")

        technology_ids = request.technology_ids()
        if technology_ids:
            technologies = self.technology_repository.find_all_by_id_in(technology_ids)
            if len(technologies) != len(technology_ids):
                raise BadRequestException("Uma ou mais tecnologias informadas não existem.")

        return self.project_repository.save(
            request.title,
            request.description,
            request.repository_url,
            profile_id,
            technology_ids,
        )

    def find_by_id(self, id_: int) -> Project:
        project = self.project_repository.find_with_details_by_id(id_)
        if project is None:
            raise NotFoundException("Projeto não encontrado.")

        return project

    def find_all(self, profile_id: Optional[int]) -> list[Project]:
        if profile_id is not None:
            return self.project_repository.find_all_by_profile_id(profile_id)

        return self.project_repository.find_all_order_by_created_at_desc()
