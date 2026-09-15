from __future__ import annotations

from app.dto.requests import ProfileCreateRequest
from app.entities import Profile
from app.exceptions import ConflictException, NotFoundException
from app.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository) -> None:
        self.profile_repository = profile_repository

    def create(self, request: ProfileCreateRequest) -> Profile:
        if self.profile_repository.find_by_email(request.email) is not None:
            raise ConflictException("Já existe um perfil cadastrado com este e-mail.")

        return self.profile_repository.save(request.name, request.email, request.bio, request.avatar_url)

    def find_by_id(self, id_: int) -> Profile:
        profile = self.profile_repository.find_with_projects_by_id(id_)
        if profile is None:
            raise NotFoundException("Perfil não encontrado.")

        return profile
