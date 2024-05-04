from uuid import uuid4
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

async def test_get_user_validation_error(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test",
        "is_active": True}
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id=123")
    assert resp.status_code == 422
    data_from_resp = resp.json()
    assert data_from_resp == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            }
        ]
    }

async def test_get_user_not_found(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "username": "tester",
        "first_name": "Test",
        "last_name": "Testovich",
        "email": "test@test",
        "is_active": True}
    user_id_for_finding = uuid4()
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_id_for_finding}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id_for_finding} not found"}