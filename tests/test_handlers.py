import pytest
import json
from tests.conftest import create_test_auth_headers_for_user
from datetime import date, timedelta
import requests


async def test_create_user(client, get_user_from_database):
    user_data = {
            "username": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password": "string",
            "salary_amount": 1000
        }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["first_name"] == user_data["first_name"]
    assert data_from_resp["last_name"] == user_data["last_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
async def test_get_user_salary(client, get_user_from_database):
    user_data = {
            "username": "stringgg",
            "first_name": "string",
            "last_name": "string",
            "email": "userrr@example.com",
            "password": "string",
            "salary_amount": 100
        }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["first_name"] == user_data["first_name"]
    assert data_from_resp["last_name"] == user_data["last_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    response = client.post("/login/token", data={"username": "stringgg", "password": "string"})
    assert response.status_code == 200

async def test_get_user_salary(client, get_user_from_database):
    user_data = {
            "username": "stringg",
            "first_name": "stringg",
            "last_name": "stringg",
            "email": "userr@example.com",
            "password": "stringg",
            "salary_amount": 100
        }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["first_name"] == user_data["first_name"]
    assert data_from_resp["last_name"] == user_data["last_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    response = client.post("/login/token", data={"username": "stringg", "password": "stringg"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    salary_response = client.get("/login/salary", headers=headers)
    assert salary_response.status_code == 200
    salary_data = salary_response.json()
    assert salary_data["salary_amount"] == user_data["salary_amount"]
    assert salary_data["next_raise_date"] == str(date.today() + timedelta(days=365))

