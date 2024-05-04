from uuid import uuid4
import json
import pytest
async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test",
        "is_active": True
    }
    user_data_updated = {
      "first_name": "Ivan",
      "last_name": "Ivanov",
      "email": "keker@gmail.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data_updated["username"]
    assert user_from_db["first_name"] == user_data_updated["first_name"]
    assert user_from_db["last_name"] == user_data_updated["last_name"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]

async def test_update_user_check_one_is_updated(client, create_user_in_database, get_user_from_database):
    user_data_1 = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test.com",
        "is_active": True
    }
    user_data_2 = {
        "user_id": uuid4(),
        "username": "ivanus",
        "first_name": "Ivan",
        "last_name": "Ivanovich",
        "email": "ivan@test.com",
        "is_active": True
    }
    user_data_3 = {
        "user_id": uuid4(),
        "username": "semus",
        "first_name": "Semen",
        "last_name": "Semenovich",
        "email": "semen@test.com",
        "is_active": True
    }
    user_data_updated = {
        "first_name": "Prokiofiy",
        "last_name": "Ivanovich",
        "email": "belyash@test.com"
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    users_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data_1["username"]
    assert user_from_db["first_name"] == user_data_updated["first_name"]
    assert user_from_db["last_name"] == user_data_updated["last_name"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_1["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]
    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data_2["username"]
    assert user_from_db["first_name"] == user_data_2["first_name"]
    assert user_from_db["last_name"] == user_data_2["last_name"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]
    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data_3["username"]
    assert user_from_db["first_name"] == user_data_3["first_name"]
    assert user_from_db["last_name"] == user_data_3["last_name"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]

@pytest.mark.parametrize("user_data_updated, expected_status_code, expected_detail", [
    (
            {},
            422,
            {"detail": "At least one parameter for user update info should be provided"}
    ),
    (
            {"name": "123"},
            422,
            {"detail": "Name should contains only letters"}
    ),
    (
            {"email": ""},
            422,
            {'detail':  [{'loc': ['body', 'email'],
                          'msg': 'value is not a valid email address',
                          'type': 'value_error.email'
                          }]
             }
    ),
    (
            {"surname": ""},
            422,
            {'detail': [{'loc': ['body', 'surname'], 'msg': 'ensure this value has at least 1 characters',
                         'type': 'value_error.any_str.min_length', 'ctx': {'limit_value': 1}}]}
    ),
    (
            {"name": ""},
            422,
            {'detail': [{'loc': ['body', 'name'], 'msg': 'ensure this value has at least 1 characters',
                         'type': 'value_error.any_str.min_length', 'ctx': {'limit_value': 1}}]}
    ),
    (
            {"surname": "123"},
            422,
            {"detail": "Surname should contains only letters"}
    ),
    (
            {"email": "123"},
            422,
            {'detail': [{'loc': ['body', 'email'], 'msg': 'value is not a valid email address',
                         'type': 'value_error.email'}]}
    )
])
async def test_update_user_validation_error(client, create_user_in_database, get_user_from_database, user_data_updated,
                                            expected_status_code, expected_detail):
    user_data = {
        "user_id": uuid4(),
        "username": "userivan",
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "email": "lol2@gmail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test.com"
    }
    user_data_2 = {
        "user_id": uuid4(),
        "username": "ivanus",
        "first_name": "Ivan",
        "last_name": "Ivanovich",
        "email": "ivan@test.com"
    }
    user_data_update = {
        "email": user_data_2["email"]
    }
    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_update))
    assert resp.status_code == 503
    assert 'duplicate key value violates unique constraint "users_email_key"' in resp.json()["detail"]

