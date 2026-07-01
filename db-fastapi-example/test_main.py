import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """
    Her test için geçici bir SQLite veritabanı oluşturur.
    Gerçek courses.db dosyasına dokunmaz.
    """

    test_db_path = tmp_path / "test_courses.db"

    monkeypatch.setattr(main, "DB_PATH", test_db_path)

    conn = main.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            level TEXT NOT NULL,
            price REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO courses (title, description, level, price)
        VALUES (?, ?, ?, ?)
        """,
        (
            "Python Eğitimi",
            "Python temellerini anlatan eğitim",
            "beginner",
            100.0,
        ),
    )

    conn.commit()
    conn.close()

    return TestClient(main.app)


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FastAPI SQLite CRUD API"
    }


def test_list_courses(client):
    response = client.get("/courses")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]["id"] == 1
    assert data[0]["title"] == "Python Eğitimi"
    assert data[0]["description"] == "Python temellerini anlatan eğitim"
    assert data[0]["level"] == "beginner"
    assert data[0]["price"] == 100.0


def test_get_course_by_id(client):
    response = client.get("/courses/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Python Eğitimi"
    assert data["level"] == "beginner"
    assert data["price"] == 100.0


def test_get_course_not_found(client):
    response = client.get("/courses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Eğitim bulunamadı"


def test_create_course(client):
    new_course = {
        "title": "FastAPI Eğitimi",
        "description": "FastAPI ile backend geliştirme eğitimi",
        "level": "intermediate",
        "price": 250.0
    }

    response = client.post("/courses", json=new_course)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 2
    assert data["title"] == "FastAPI Eğitimi"
    assert data["description"] == "FastAPI ile backend geliştirme eğitimi"
    assert data["level"] == "intermediate"
    assert data["price"] == 250.0


def test_create_course_validation_error_short_title(client):
    invalid_course = {
        "title": "Py",
        "description": "Python temellerini anlatan eğitim",
        "level": "beginner",
        "price": 100.0
    }

    response = client.post("/courses", json=invalid_course)

    assert response.status_code == 422


def test_create_course_validation_error_negative_price(client):
    invalid_course = {
        "title": "Python Eğitimi",
        "description": "Python temellerini anlatan eğitim",
        "level": "beginner",
        "price": -10
    }

    response = client.post("/courses", json=invalid_course)

    assert response.status_code == 422


def test_create_course_validation_error_wrong_level(client):
    invalid_course = {
        "title": "Python Eğitimi",
        "description": "Python temellerini anlatan eğitim",
        "level": "easy",
        "price": 100
    }

    response = client.post("/courses", json=invalid_course)

    assert response.status_code == 422


def test_update_course(client):
    updated_course = {
        "title": "Güncel Python Eğitimi",
        "description": "Python konularını güncel şekilde anlatan eğitim",
        "level": "advanced",
        "price": 300.0
    }

    response = client.put("/courses/1", json=updated_course)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Güncel Python Eğitimi"
    assert data["description"] == "Python konularını güncel şekilde anlatan eğitim"
    assert data["level"] == "advanced"
    assert data["price"] == 300.0


def test_update_course_not_found(client):
    updated_course = {
        "title": "Güncel Python Eğitimi",
        "description": "Python konularını güncel şekilde anlatan eğitim",
        "level": "advanced",
        "price": 300.0
    }

    response = client.put("/courses/999", json=updated_course)

    assert response.status_code == 404
    assert response.json()["detail"] == "Eğitim bulunamadı"


def test_update_course_validation_error(client):
    invalid_course = {
        "title": "Py",
        "description": "Kısa",
        "level": "advanced",
        "price": -50
    }

    response = client.put("/courses/1", json=invalid_course)

    assert response.status_code == 422