from __future__ import annotations


def test_create_returns_created_technology(client):
    response = client.post("/api/technologies", json={"name": "Python"})
    body = response.get_json()

    assert response.status_code == 201
    assert body["name"] == "Python"
    assert body["id"] is not None


def test_create_without_name_returns_validation_error(client):
    response = client.post("/api/technologies", json={})
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "name" é obrigatório.' in body["errors"]


def test_create_with_blank_name_returns_validation_error(client):
    response = client.post("/api/technologies", json={"name": "   "})
    body = response.get_json()

    assert response.status_code == 400
    assert 'O campo "name" é obrigatório.' in body["errors"]


def test_create_with_duplicated_name_returns_conflict(client):
    client.post("/api/technologies", json={"name": "Python"})
    response = client.post("/api/technologies", json={"name": "Python"})
    body = response.get_json()

    assert response.status_code == 409
    assert body["message"] == "Já existe uma tecnologia cadastrada com este nome."


def test_find_all_returns_empty_list_when_none_exists(client):
    response = client.get("/api/technologies")

    assert response.status_code == 200
    assert response.get_json() == []


def test_find_all_returns_technologies_ordered_by_name(client):
    client.post("/api/technologies", json={"name": "Flask"})
    client.post("/api/technologies", json={"name": "Docker"})

    response = client.get("/api/technologies")
    body = response.get_json()

    assert response.status_code == 200
    assert [technology["name"] for technology in body] == ["Docker", "Flask"]
