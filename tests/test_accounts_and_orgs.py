def test_accounts_list_forbidden_for_member(auth_client_factory, member):
    c = auth_client_factory(member)
    rsp = c.get("/api/accounts/")
    assert rsp.status_code == 403

def test_accounts_list_allowed_for_saas(auth_client_factory, saas_admin):
    c = auth_client_factory(saas_admin)
    rsp = c.get("/api/accounts/")
    assert rsp.status_code == 200

def test_org_list_under_account_forbidden_member(auth_client_factory, member, account):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/accounts/{account.id}/organizations/")
    assert rsp.status_code == 403

def test_org_list_under_account_allowed_saas(auth_client_factory, saas_admin, account):
    c = auth_client_factory(saas_admin)
    rsp = c.get(f"/api/accounts/{account.id}/organizations/")
    assert rsp.status_code == 200

def test_org_retrieve_own_allowed_member(auth_client_factory, member, org1, account):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/accounts/{org1.account_id}/organizations/{org1.id}/")
    assert rsp.status_code == 200
    assert rsp.json()["organizationId"] == org1.id

def test_org_retrieve_other_forbidden_member(auth_client_factory, member, org2, account):
    c = auth_client_factory(member)
    rsp = c.get(f"/api/accounts/{org2.account_id}/organizations/{org2.id}/")
    assert rsp.status_code in (403, 404)
