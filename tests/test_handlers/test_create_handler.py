import pytest
import json

async def test_create_user(client, get_user_from_database):
    user_data = {
        "username": "entozhevlad",
        "first_name": "Vladislav",
        "last_name": "Zarubin",
        "email": "test@gmail.com"
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

async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {
        "username": "entozhevlad",
        "first_name": "Vladislav",
        "last_name": "Zarubin",
        "email": "test@gmail.com" }
    user_data_same_email = {
        "username": "entozheclone",
        "first_name": "Nelson",
        "last_name": "Mandela",
        "email": "test@gmail.com"
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
    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    assert (
        resp.json()["detail"]
        == f"Пользователь с email {user_data_same_email['email']} уже существует"
    )
@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "surname"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "email"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "password"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            {"name": 123, "surname": 456, "email": "lol"},
            422,
            {"detail": "Name should contains only letters"},
        ),
        (
            {"name": "Nikolai", "surname": 456, "email": "lol"},
            422,
            {"detail": "Surname should contains only letters"},
        ),
        (
            {"name": "Nikolai", "surname": "Sviridov", "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    },
                    {
                        "loc": ["body", "password"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
    ],
)
async def test_create_user_validation_error(
    client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail
