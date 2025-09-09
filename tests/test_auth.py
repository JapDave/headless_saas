from .conftest import DEFAULT_PASSWORD

def test_token_obtain_success(api_client, saas_admin):
    rsp = api_client.post("/api/auth/token/", {
        "username": saas_admin.username,
        "password": DEFAULT_PASSWORD
    }, format="json")
    assert rsp.status_code == 200
    data = rsp.json()
    assert "access" in data and "refresh" in data

def test_token_obtain_fail_wrong_password(api_client, saas_admin):
    rsp = api_client.post("/api/auth/token/", {
        "username": saas_admin.username,
        "password": "WrongP@ss!"
    }, format="json")
    assert rsp.status_code in (400, 401, 403)
