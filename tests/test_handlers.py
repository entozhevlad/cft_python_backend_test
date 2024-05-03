import json
import asyncio


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
    assert users_from_db["first_name"] == user_data["first_name"]
    assert users_from_db["last_name"] == user_data["last_name"]
    assert users_from_db["email"] == user_data["email"]
    assert users_from_db["is_active"] is True
    assert str(users_from_db["user_id"]) == data_from_resp["user_id"]


