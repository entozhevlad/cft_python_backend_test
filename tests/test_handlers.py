import json
import asyncio
import pytest
import json
from uuid import uuid4
from sqlalchemy.sql import text

async def test_create_user(client, get_user_from_database):
    user_data = {
        "username": "entozhevlad",
        "first_name": "Vladislav",
        "last_name": "Zarubin",
        "email": "nikolossjakson@gmail.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["first_name"] == user_data["first_name"]
    assert data_from_resp["last_name"] == user_data["last_name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data["username"]
    assert user_from_db["first_name"] == user_data["first_name"]
    assert user_from_db["last_name"] == user_data["last_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data["username"]
    assert user_from_db["first_name"] == user_data["first_name"]
    assert user_from_db["last_name"] == user_data["last_name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]

async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test",
        "is_active": True}
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["username"] == str(user_data["username"])
    assert user_from_response["first_name"] == str(user_data["first_name"])
    assert user_from_response["last_name"] == str(user_data["last_name"])
    assert user_from_response["email"] == str(user_data["email"])
    assert user_from_response["is_active"] is True
