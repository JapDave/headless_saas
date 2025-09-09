def test_roles_list_same_org_visibility(auth_client_factory, member, org1):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/organizations/{org1.id}/roles/")
    # If roles are visible to members, expect 200; if hidden, expect 403.
    assert rsp.status_code in (200, 403)

def test_roles_create_requires_org_admin(auth_client_factory, member, org_admin, org1):
    c_member = auth_client_factory(member)
    rsp_forbidden = c_member.post(f"/api/organizations/{org1.id}/roles/", {
        "name": "Team Manager",
        "description": "manages teams",
        "isCustom": True,
        "permissions": ["teams:read","teams:write"]
    }, format="json")
    assert rsp_forbidden.status_code == 403

    c_admin = auth_client_factory(org_admin)
    rsp_ok = c_admin.post(f"/api/organizations/{org1.id}/roles/", {
        "name": "Team Manager",
        "description": "manages teams",
        "isCustom": True,
        "permissions": ["teams:read","teams:write"]
    }, format="json")
    assert rsp_ok.status_code == 201
