import requests


def test_endpoint_is_available():
    response = requests.get("http://127.0.0.1:8000/user/?user_id=10f9bf9f-f352-46e1-a68e-ad1d934399d3")
    assert response.status_code == 200
