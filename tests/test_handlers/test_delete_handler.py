from fastapi.testclient import TestClient
from main import app  # Замените "your_main_module" на имя вашего основного модуля FastAPI

client = TestClient(app)

def test_create_user():
    user_data = {
        "username": "stringerr",
        "first_name": "string",
        "last_name": "stringovich",
        "email": "usermaiil@example.com",
        "password": "string",
        "salary_amount": 10000
    }
    response = client.post("/user/", json=user_data)
    assert response.status_code == 200  # Убедитесь, что код состояния HTTP равен 200 (Успех)
    assert response.json()["username"] == "stringerr"  # Проверьте, что созданный пользователь имеет ожидаемое имя пользователя
    # Другие проверки, если необходимо

# from uuid import uuid4
# async def test_delete_user(client, create_user_in_database, get_user_from_database):
#     user_data = {
#         "user_id": uuid4(),
#         "username": "tester",
#         "first_name": "Test",
#         "last_name": "Testovich",
#         "email": "test@test.com",
#         "is_active": True
#     }
#     await create_user_in_database(**user_data)
#     resp = client.delete(f"/user/?user_id={user_data['user_id']}")
#     assert resp.status_code == 200
#     assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
#     users_from_db = await get_user_from_database(user_data["user_id"])
#     user_from_db = dict(users_from_db[0])
#     assert user_from_db["username"] == user_data["username"]
#     assert user_from_db["first_name"] == user_data["first_name"]
#     assert user_from_db["last_name"] == user_data["last_name"]
#     assert user_from_db["email"] == user_data["email"]
#     assert user_from_db["is_active"] is False
#     assert user_from_db["user_id"] == user_data["user_id"]
#
# async def test_delete_user_not_found(client):
#     user_id= uuid4()
#     resp = client.delete(f"/user/?user_id={user_id}")
#     assert resp.status_code == 404
#     assert resp.json() == {"detail": f"User with id {user_id} not found"}
#
# async def test_get_user_user_id_validation_error(client):
#     resp = client.get(f"/user/?user_id=123")
#     assert resp.status_code == 422
#     data_from_resp = resp.json()
#     assert data_from_resp == {
#         "detail": [
#             {
#                 "loc": ["query", "user_id"],
#                 "msg": "value is not a valid uuid",
#                 "type": "type_error.uuid"
#             }
#         ]
#     }