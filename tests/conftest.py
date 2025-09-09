import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import Account, Organization
from roles.models import Role, UserRole

DEFAULT_PASSWORD = "StrongP@ss1!"

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def account(db):
    return Account.objects.create(name="Acme", description="Test acct")

@pytest.fixture
def org1(db, account):
    return Organization.objects.create(account=account, name="Org A")

@pytest.fixture
def org2(db, account):
    return Organization.objects.create(account=account, name="Org B")

@pytest.fixture
def saas_admin(db):
    User = get_user_model()
    u = User.objects.create(
        username="saas@example.com",
        email="saas@example.com",
        is_staff=True,
        status="active",
    )
    u.set_password(DEFAULT_PASSWORD)
    u.save()
    return u

@pytest.fixture
def org_admin_role(db, org1):
    return Role.objects.create(organization=org1, name="Org Admin", is_custom=False, permissions=["*"])

@pytest.fixture
def org_admin(db, org1, org_admin_role):
    User = get_user_model()
    u = User.objects.create(
        username="oa@example.com",
        email="oa@example.com",
        organization=org1,
        status="active",
    )
    u.set_password(DEFAULT_PASSWORD)
    u.save()
    UserRole.objects.create(user=u, role=org_admin_role)
    return u

@pytest.fixture
def member(db, org1):
    User = get_user_model()
    u = User.objects.create(
        username="member1@example.com",
        email="member1@example.com",
        organization=org1,
        status="active",
    )
    u.set_password(DEFAULT_PASSWORD)
    u.save()
    return u

@pytest.fixture
def member_other_org(db, org2):
    User = get_user_model()
    u = User.objects.create(
        username="member2@example.com",
        email="member2@example.com",
        organization=org2,
        status="active",
    )
    u.set_password(DEFAULT_PASSWORD)
    u.save()
    return u

@pytest.fixture
def auth_client_factory(api_client):
    def _make(user):
        resp = api_client.post("/api/auth/token/", {
            "username": user.username,
            "password": DEFAULT_PASSWORD
        }, format="json")
        assert resp.status_code == 200, f"Token failed for {user.username}: {resp.status_code} {resp.content}"
        access = resp.json()["access"]
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return c
    return _make

@pytest.fixture
def org(org1):
    """Alias so tests that expect 'org' keep working."""
    return org1