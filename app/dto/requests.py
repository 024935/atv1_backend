"""DTOs de entrada: normalizam o corpo da requisição e validam os campos obrigatórios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.validation.validator import Validator


@dataclass
class ProfileCreateRequest:
    name: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "ProfileCreateRequest":
        request = cls(
            name=str(data["name"]) if data.get("name") is not None else None,
            email=str(data["email"]) if data.get("email") is not None else None,
            bio=str(data["bio"]) if data.get("bio") is not None else None,
            avatar_url=(
                str(data["avatarUrl"])
                if data.get("avatarUrl") not in (None, "")
                else None
            ),
        )

        Validator() \
            .not_blank(request.name, 'O campo "name" é obrigatório.') \
            .max_length(request.name, 120, 'O campo "name" deve ter no máximo 120 caracteres.') \
            .not_blank(request.email, 'O campo "email" é obrigatório.') \
            .email(request.email, 'O campo "email" deve ser um e-mail válido.') \
            .max_length(request.bio, 1000, 'O campo "bio" deve ter no máximo 1000 caracteres.') \
            .url(request.avatar_url, 'O campo "avatarUrl" deve ser uma URL válida.', optional=True) \
            .validate()

        return request


@dataclass
class TechnologyCreateRequest:
    name: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "TechnologyCreateRequest":
        request = cls(name=str(data["name"]) if data.get("name") is not None else None)

        Validator() \
            .not_blank(request.name, 'O campo "name" é obrigatório.') \
            .max_length(request.name, 60, 'O campo "name" deve ter no máximo 60 caracteres.') \
            .validate()

        return request


@dataclass
class ProjectCreateRequest:
    title: Optional[str]
    description: Optional[str]
    repository_url: Optional[str]
    profile_id_raw: Any
    technology_ids_raw: list

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectCreateRequest":
        raw_technology_ids = data.get("technologyIds")

        request = cls(
            title=str(data["title"]) if data.get("title") is not None else None,
            description=str(data["description"]) if data.get("description") is not None else None,
            repository_url=str(data["repositoryUrl"]) if data.get("repositoryUrl") is not None else None,
            profile_id_raw=data.get("profileId"),
            technology_ids_raw=raw_technology_ids if isinstance(raw_technology_ids, list) else [],
        )

        Validator() \
            .not_blank(request.title, 'O campo "title" é obrigatório.') \
            .max_length(request.title, 150, 'O campo "title" deve ter no máximo 150 caracteres.') \
            .max_length(request.description, 2000, 'O campo "description" deve ter no máximo 2000 caracteres.') \
            .not_blank(request.repository_url, 'O campo "repositoryUrl" é obrigatório.') \
            .url(request.repository_url, 'O campo "repositoryUrl" deve ser uma URL válida.') \
            .not_null(request.profile_id_raw, 'O campo "profileId" é obrigatório.') \
            .positive(request.profile_id_raw, 'O campo "profileId" deve ser um número positivo.') \
            .positive_list(raw_technology_ids, 'Os itens de "technologyIds" devem ser números positivos.') \
            .validate()

        return request

    def profile_id(self) -> int:
        return int(self.profile_id_raw)

    def technology_ids(self) -> list[int]:
        return [int(technology_id) for technology_id in self.technology_ids_raw]
