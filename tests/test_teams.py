def test_teams_read_same_org(auth_client_factory, member, org1):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/organizations/{org1.id}/teams/")
    assert rsp.status_code == 200

def test_teams_create_requires_org_admin(auth_client_factory, member, org_admin, org1):
    c_member = auth_client_factory(member)
    rsp_forbidden = c_member.post(f"/api/organizations/{org1.id}/teams/", {
        "name": "Support",
        "description": "24x7"
    }, format="json")
    assert rsp_forbidden.status_code == 403

    c_admin = auth_client_factory(org_admin)
    rsp_ok = c_admin.post(f"/api/organizations/{org1.id}/teams/", {
        "name": "Support",
        "description": "24x7"
    }, format="json")
    assert rsp_ok.status_code == 201
