from .conftest import DEFAULT_PASSWORD

def test_users_list_same_org_allowed_member(auth_client_factory, member, org1):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/organizations/{org1.id}/users/")
    assert rsp.status_code == 200

def test_users_create_same_org_forbidden_member(auth_client_factory, member, org1):
    c = auth_client_factory(member)
    payload = {
        "email": "newuser@example.com",
        "fullName": "New User",
        "status": "active",
        "password": DEFAULT_PASSWORD
    }
    rsp = c.post(f"/api/organizations/{org1.id}/users/", payload, format="json")
    assert rsp.status_code == 403

def test_users_create_same_org_allowed_org_admin(auth_client_factory, org_admin, org1):
    c = auth_client_factory(org_admin)
    payload = {
        "email": "orgadmin-created@example.com",
        "fullName": "OA Created",
        "status": "active",
        "password": DEFAULT_PASSWORD
    }
    rsp = c.post(f"/api/organizations/{org1.id}/users/", payload, format="json")
    assert rsp.status_code == 201
    body = rsp.json()
    assert body["email"] == "orgadmin-created@example.com"

def test_users_write_cross_org_forbidden_org_admin(auth_client_factory, org_admin, org2):
    c = auth_client_factory(org_admin)
    payload = {
        "email": "cross@example.com",
        "fullName": "Cross Org",
        "status": "active",
        "password": DEFAULT_PASSWORD
    }
    rsp = c.post(f"/api/organizations/{org2.id}/users/", payload, format="json")
    assert rsp.status_code == 403
