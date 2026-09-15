from __future__ import annotations


def test_create_returns_created_profile(client):
    response = client.post(
        "/api/profiles",
        json={
            "name": "Ana Souza",
            "email": "ana@example.com",
            "bio": "Dev backend apaixonada por APIs",
            "avatarUrl": "https://example.com/ana.png",
        },
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body["name"] == "Ana Souza"
    assert body["email"] == "ana@example.com"
    assert body["projects"] == []
    assert body["id"] is not None


def test_create_without_name_returns_validation_error(client):
    response = client.post("/api/profiles", json={"email": "sem-nome@example.com"})
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Erro de validação."
    assert 'O campo "name" é obrigatório.' in body["errors"]


def test_create_with_blank_name_returns_validation_error(client):
    response = client.post("/api/profiles", json={"name": "   ", "email": "em-branco@example.com"})
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "name" é obrigatório.' in body["errors"]


def test_create_with_invalid_email_returns_validation_error(client):
    response = client.post("/api/profiles", json={"name": "Carlos", "email": "nao-e-um-email"})
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "email" deve ser um e-mail válido.' in body["errors"]


def test_create_with_duplicated_email_returns_conflict(client):
    client.post("/api/profiles", json={"name": "Carlos", "email": "carlos@example.com"})
    response = client.post("/api/profiles", json={"name": "Outro Carlos", "email": "carlos@example.com"})
    body = response.get_json()

    assert response.status_code == 409
    assert body["message"] == "Já existe um perfil cadastrado com este e-mail."


def test_find_by_id_returns_profile_with_projects(client):
    created = client.post("/api/profiles", json={"name": "Bia", "email": "bia@example.com"}).get_json()

    response = client.get(f"/api/profiles/{created['id']}")
    body = response.get_json()

    assert response.status_code == 200
    assert body["name"] == "Bia"
    assert body["projects"] == []


def test_find_by_id_not_found_returns_404(client):
    response = client.get("/api/profiles/999")
    body = response.get_json()

    assert response.status_code == 404
    assert body["message"] == "Perfil não encontrado."
