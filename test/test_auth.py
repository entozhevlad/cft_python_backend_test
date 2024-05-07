import pytest
from sqlalchemy import insert, select
from conftest import client, async_session_maker

def test_register():
    client.post("/user/", json={
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "email": "user@example.com",
      "password": "string",
      "salary_amount": 100
        })