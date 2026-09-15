from __future__ import annotations

from app.dto.requests import TechnologyCreateRequest
from app.entities import Technology
from app.exceptions import ConflictException
from app.repositories.technology_repository import TechnologyRepository


class TechnologyService:
    def __init__(self, technology_repository: TechnologyRepository) -> None:
        self.technology_repository = technology_repository

    def create(self, request: TechnologyCreateRequest) -> Technology:
        if self.technology_repository.find_by_name(request.name) is not None:
            raise ConflictException("Já existe uma tecnologia cadastrada com este nome.")

        return self.technology_repository.save(request.name)

    def find_all(self) -> list[Technology]:
        return self.technology_repository.find_all_order_by_name()
