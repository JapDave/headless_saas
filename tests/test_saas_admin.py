def test_saas_admin_can_manage_everything(auth_client_factory, saas_admin, account):
    c = auth_client_factory(saas_admin)
    assert c.get("/api/accounts/").status_code == 200
    # Create organization under account
    rsp = c.post(f"/api/accounts/{account.id}/organizations/", {
        "name": "New Org",
        "description": "created by saas",
        "logoUrl": ""
    }, format="json")
    assert rsp.status_code == 201
