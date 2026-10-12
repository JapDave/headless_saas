import pytest
from teams.models import Team


@pytest.mark.django_db
@pytest.mark.parametrize("resource,payload", [
    ("teams", {"name": "Support"}),
    ("roles", {"name": "Reviewer"}),
    ("users", {"email": "new@example.com", "password": "StrongP@ss1!"}),
])
def test_create_rejects_foreign_organization(auth_client_factory, org_admin, org1, org2, resource, payload):
    client = auth_client_factory(org_admin)
    payload["organizationId"] = org2.id
    response = client.post(f"/api/organizations/{org1.id}/{resource}/", payload, format="json")
    assert response.status_code == 400
    assert "organizationId" in response.json()


@pytest.mark.django_db
def test_update_cannot_move_team_to_foreign_organization(auth_client_factory, org_admin, org1, org2):
    team = Team.objects.create(organization=org1, name="Support")
    response = auth_client_factory(org_admin).patch(
        f"/api/organizations/{org1.id}/teams/{team.id}/", {"organizationId": org2.id}, format="json"
    )
    assert response.status_code == 400
    team.refresh_from_db()
    assert team.organization_id == org1.id


@pytest.mark.django_db
def test_user_without_password_cannot_login(auth_client_factory, org_admin, org1):
    from users.models import User
    response = auth_client_factory(org_admin).post(
        f"/api/organizations/{org1.id}/users/", {"email": "invited@example.com"}, format="json"
    )
    assert response.status_code == 201
    assert not User.objects.get(email="invited@example.com").has_usable_password()
