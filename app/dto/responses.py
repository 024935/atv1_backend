"""DTOs de saída: moldam as entidades de domínio no formato JSON exposto pela API."""

from __future__ import annotations

from app.entities import Feedback, Profile, Project, Technology


def feedback_summary(feedback: Feedback) -> dict:
    return {
        "id": feedback.id,
        "comment": feedback.comment,
        "rating": feedback.rating,
    }


def profile_summary(profile: Profile) -> dict:
    return {
        "id": profile.id,
        "name": profile.name,
        "email": profile.email,
    }


def project_summary(project: Project) -> dict:
    return {
        "id": project.id,
        "title": project.title,
    }


def technology_response(technology: Technology) -> dict:
    return {
        "id": technology.id,
        "name": technology.name,
        "createdAt": technology.created_at,
        "updatedAt": technology.updated_at,
    }


def profile_response(profile: Profile) -> dict:
    return {
        "id": profile.id,
        "name": profile.name,
        "email": profile.email,
        "bio": profile.bio,
        "avatarUrl": profile.avatar_url,
        "projects": [project_summary(project) for project in profile.projects],
        "createdAt": profile.created_at,
        "updatedAt": profile.updated_at,
    }


def project_response(project: Project) -> dict:
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "repositoryUrl": project.repository_url,
        "profile": profile_summary(project.profile) if project.profile is not None else None,
        "technologies": [technology_response(technology) for technology in project.technologies],
        "feedbacks": [feedback_summary(feedback) for feedback in project.feedbacks],
        "createdAt": project.created_at,
        "updatedAt": project.updated_at,
    }
