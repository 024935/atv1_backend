from __future__ import annotations


def _create_profile(client, email: str = "flavio@example.com") -> int:
    response = client.post("/api/profiles", json={"name": "Flavio Rocha", "email": email})

    return response.get_json()["id"]


def _create_technology(client, name: str) -> int:
    response = client.post("/api/technologies", json={"name": name})

    return response.get_json()["id"]


def test_create_returns_created_project_with_relations(client):
    profile_id = _create_profile(client)
    technology_id = _create_technology(client, "Python")

    response = client.post(
        "/api/projects",
        json={
            "title": "DevShowcase API",
            "description": "Backend do projeto",
            "repositoryUrl": "https://github.com/dev/devshowcase",
            "profileId": profile_id,
            "technologyIds": [technology_id],
        },
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body["title"] == "DevShowcase API"
    assert body["profile"]["id"] == profile_id
    assert [technology["name"] for technology in body["technologies"]] == ["Python"]
    assert body["feedbacks"] == []


def test_create_without_title_returns_validation_error(client):
    profile_id = _create_profile(client)

    response = client.post(
        "/api/projects",
        json={"repositoryUrl": "https://github.com/dev/devshowcase", "profileId": profile_id},
    )
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "title" é obrigatório.' in body["errors"]


def test_create_with_blank_title_returns_validation_error(client):
    profile_id = _create_profile(client)

    response = client.post(
        "/api/projects",
        json={
            "title": "   ",
            "repositoryUrl": "https://github.com/dev/devshowcase",
            "profileId": profile_id,
        },
    )
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "title" é obrigatório.' in body["errors"]


def test_create_with_invalid_repository_url_returns_validation_error(client):
    profile_id = _create_profile(client)

    response = client.post(
        "/api/projects",
        json={"title": "Projeto X", "repositoryUrl": "nao-e-uma-url", "profileId": profile_id},
    )
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "repositoryUrl" deve ser uma URL válida.' in body["errors"]


def test_create_with_unknown_profile_returns_bad_request(client):
    response = client.post(
        "/api/projects",
        json={"title": "Projeto X", "repositoryUrl": "https://github.com/dev/x", "profileId": 999},
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Profile com id 999 não encontrado."


def test_create_with_unknown_technology_returns_bad_request(client):
    profile_id = _create_profile(client)

    response = client.post(
        "/api/projects",
        json={
            "title": "Projeto X",
            "repositoryUrl": "https://github.com/dev/x",
            "profileId": profile_id,
            "technologyIds": [999],
        },
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Uma ou mais tecnologias informadas não existem."


def test_find_all_returns_all_projects(client):
    profile_id = _create_profile(client)
    client.post(
        "/api/projects",
        json={"title": "Projeto A", "repositoryUrl": "https://github.com/dev/a", "profileId": profile_id},
    )
    client.post(
        "/api/projects",
        json={"title": "Projeto B", "repositoryUrl": "https://github.com/dev/b", "profileId": profile_id},
    )

    response = client.get("/api/projects")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body) == 2


def test_find_all_filters_by_profile_id(client):
    profile_a = _create_profile(client, "a@example.com")
    profile_b = _create_profile(client, "b@example.com")
    client.post(
        "/api/projects",
        json={"title": "Projeto A", "repositoryUrl": "https://github.com/dev/a", "profileId": profile_a},
    )
    client.post(
        "/api/projects",
        json={"title": "Projeto B", "repositoryUrl": "https://github.com/dev/b", "profileId": profile_b},
    )

    response = client.get(f"/api/projects?profileId={profile_a}")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["title"] == "Projeto A"
