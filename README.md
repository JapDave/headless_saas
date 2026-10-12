# Headless SaaS API (Django REST + Docker)

Django REST reference implementation implementing **Accounts → Organizations → Users → Teams** with **Roles (RBAC)** and **Subscriptions**, JWT auth, soft-delete, pagination & filtering, and auto OpenAPI docs (Swagger & Redoc).

> API fields follow the spec’s **camelCase** (e.g., `accountId`, `createdAt`), while Django models remain Pythonic (`snake_case`). Serializers map between them so the external contract stays exactly as required.

---

## Table of contents

- [Architecture & hierarchy](#architecture--hierarchy)  
- [Access model (permissions)](#access-model-permissions)  
- [End-to-end flows](#end-to-end-flows)  
- [Assumptions (and how to change them)](#assumptions-and-how-to-change-them)  
- [Setup & run](#setup--run)  
- [Getting a token & using Swagger](#getting-a-token--using-swagger)  
- [API quickstart (spec-compliant)](#api-quickstart-spec-compliant)  
- [Running tests](#running-tests)  
- [Troubleshooting](#troubleshooting)  
- [Common variants you can enable](#common-variants-you-can-enable)

---

## Architecture & hierarchy

```
SaaS (system)
└─ Account (commercial umbrella)
   └─ Organization (tenant boundary)
      ├─ Users            (belong to exactly one org)
      ├─ Teams            (inside an org)
      ├─ Roles/UserRole   (RBAC inside an org)
      └─ Subscriptions    (plan/limits for the org)
```

- **Account**: top-level customer (contracts/billing umbrella).
- **Organization**: true **tenant** used for isolation.
- **User**: belongs to one org (simple + safe).
- **Team**: groups users within an org.
- **Role/UserRole**: org-scoped RBAC overlay.

**Soft delete** is implemented across all models via `deleted_at`; default managers hide deleted rows.

---

## Access model (permissions)

- **SaaS Admin** (system-wide): `is_staff=True` → manage everything.
- **Org Admin** (org-level): manage everything inside their organization.
- **Member**: regular user; read-only across most collections; can self-edit via `/api/me` (optional).

**Enforcement pattern (recommended):**
- **Read**: authenticated + “same org” check on org-scoped routes.
- **Write**: “same org” + elevated role (Org Admin or SaaS Admin).
- **Accounts** endpoints: SaaS Admin only.

> You can implement “Org Admin” either as a **role** (`Role` + `UserRole`) or an internal boolean flag (hidden from API). See variants below.

---

## End-to-end flows

### A) Tenant onboarding (top–down)
1) Create **Account** (SaaS Admin)  
2) Create **Organization**(s) under that Account  
3) (Recommended) Seed an **Org Admin** role for each org  
4) Create the first **Org Admin** user (or invite flow later)  

### B) User login (JWT)
1) `POST /api/auth/token/` with:
   ```json
   { "username": "admin", "password": "admin123" }
   ```
   > For users created via API, we auto-set `username = email`, so they can log in with their email under the `username` field.
2) Response returns **access** and **refresh** tokens
3) Call APIs with:
   ```
   Authorization: Bearer <ACCESS>
   ```

### C) Using Swagger
- Open `http://localhost:8000/api/docs`
- Click **Authorize** (top-right) → paste `Bearer <ACCESS>`
- Use **Try it out** on endpoints (payloads are **camelCase** as per spec)

---

## Assumptions (and how to change them)

### Tenancy & data
- **Single org per user**  
  *Assumed*: `User.organization_id` is a single FK.  
  *Change*: allow multi-org by adding a membership pivot table and scoping via memberships.

- **Unique email per org**  
  *Assumed*: `(organization_id, email)` unique.  
  *Change*: make `email` globally unique for single identity across all orgs.

- **Teams membership**  
  *Assumed*: team is a container; no `TeamMembership` yet.  
  *Change*: add `TeamMembership(user, team, role_in_team)` for explicit membership.

- **Subscriptions**  
  *Assumed*: added as a realistic SaaS resource.  
  *Change*: remove/replace with other domain object.

### Auth & login
- **JWT provider & lifetimes**  
  *Assumed*: SimpleJWT; access=60m, refresh=1d.  
  *Change*: adjust `SIMPLE_JWT` or swap to sessions/OIDC.

- **Login identifier**  
  *Assumed*: token view expects `username`; we set `username=email` automatically.  
  *Change*: make token view accept `email` directly (small serializer tweak).

- **Status enforcement**  
  *Assumed*: Django `is_active=True` required; custom `status` doesn’t block login by default.  
  *Change*: plug a status-aware token serializer to reject inactive/suspended.

### Permissions / RBAC
- **Org Admin**  
  *Assumed*: either boolean (internal) or role-based.  
  *Change*: remove boolean and enforce strictly with `Role/UserRole`.

- **Default rules**  
  *Assumed*: read = same-org; write = Org Admin or SaaS.  
  *Change*: tune per endpoint; add granular permission strings.

### API surface
- **camelCase externally / snake_case internally**  
  *Assumed*: serializers map fields; models stay Pythonic.  
  *Change*: you *can* rename DB columns, but it’s not recommended.

- **Nested org routes**  
  *Assumed*: `/organizations/{orgId}/...` and `/accounts/{accountId}/organizations/...`.  
  *Change*: flatten or version routes if needed.

### Ops / DX
- **Postgres + Docker + Gunicorn + WhiteNoise**  
  *Assumed*: production-ish baseline; `collectstatic` runs at boot.  
  *Change*: front with Nginx; add Redis/Celery, Sentry, proper logging, etc.

- **Root redirect**  
  *Assumed*: `/` → `/api/docs/` for DX.  
  *Change*: point root elsewhere or remove.

---

## Setup & run

### Docker (recommended)

```bash
# 1) Copy project, then:
cp .env.example .env

# 2) (Optional) auto-create superuser on boot
# In .env:
# AUTO_CREATE_SUPERUSER=1
# DJANGO_SUPERUSER_USERNAME=admin
# DJANGO_SUPERUSER_EMAIL=admin@example.com
# DJANGO_SUPERUSER_PASSWORD=admin123

# 3) Start
docker compose up --build
```

Endpoints:
- Swagger: `http://localhost:8000/api/docs`  
- Redoc:   `http://localhost:8000/api/redoc`  
- Admin:   `http://localhost:8000/admin/`

If you didn’t enable auto-create:
```bash
docker compose exec web python manage.py createsuperuser
```

> Static files: **WhiteNoise** + `collectstatic` is wired in the entrypoint so admin/Swagger assets are served even under Gunicorn.

### Local (venv) — optional

```bash
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

cp .env.example .env        # adjust DB vars for your local Postgres

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

---

## For running Test Cases
docker compose exec web pytest -q

## Getting a token & using Swagger

**Get tokens**  
`POST /api/auth/token/`
```json
{ "username": "admin", "password": "admin123" }
```
→ returns `{ "access": "...", "refresh": "..." }`.

**Authorize Swagger**  
Click **Authorize** → paste:
```
Bearer <ACCESS>
```

**Refresh**  
`POST /api/auth/token/refresh/`
```json
{ "refresh": "<REFRESH>" }
```

> Error “No active account found with the given credentials” = wrong username/password or `is_active=False`.  
> Error “Token has wrong type” = you used the refresh token in the `Authorization` header (should be the access token).

---

## API quickstart (spec-compliant)

All payloads/responses use **camelCase** field names matching the requirement document.

### Create Account (SaaS Admin)
`POST /api/accounts/`
```json
{
  "name": "Acme Corp",
  "description": "Enterprise customer",
  "contactEmail": "owner@acme.com",
  "isActive": true
}
```

### Create Organization under Account
`POST /api/accounts/1/organizations/`
```json
{
  "name": "Marketing",
  "description": "Global marketing",
  "logoUrl": "https://example.com/logo.png"
}
```

### Create User in Org (Org Admin or SaaS Admin)
`POST /api/organizations/1/users/`
```json
{
  "email": "jane@example.com",
  "fullName": "Jane Doe",
  "status": "active",
  "password": "StrongP@ss1!"
}
```

### Create Team (optional)
`POST /api/organizations/1/teams/`
```json
{
  "name": "Support",
  "description": "24x7 team",
  "configurations": {"sla": "gold"}
}
```

### Create Subscription (optional)
`POST /api/organizations/1/subscriptions/`
```json
{
  "productName": "Agents Platform",
  "startDate": "2025-09-01",
  "endDate": "2026-09-01",
  "status": "active",
  "planConfiguration": {"maxUsers": 50}
}
```

---

## Running tests

### Docker
```bash
docker compose exec web pytest -q
```

### Local (isolated SQLite database)
```bash
pytest --ds=config.test_settings -q
```

CI runs the same API tests against PostgreSQL. This is a backend reference project; production deployment still requires environment-specific security and operational review.

### What’s covered
- Auth smoke (obtain token and hit a protected endpoint)
- Accounts CRUD (SaaS Admin)
- Organizations nested under accounts
- Users org-scoped create/list
- Teams org-scoped create/list
- Roles org-scoped create/list

### Recommended additions
- RBAC tests (Member vs Org Admin vs SaaS Admin)
- Status-aware token tests (inactive/suspended users rejected)
- Soft-delete visibility (deleted items hidden by default)
- Filters/pagination (`?status=active`, `?page=2`)

---

## Troubleshooting

- **404 `/`** → root redirects to `/api/docs/` (verify `config/urls.py`).
- **Admin CSS missing** → ensure WhiteNoise is installed, middleware added, and `collectstatic` ran (entrypoint does this).
- **“No active account found”** → use `username` (not `email`) in the token request; confirm password; `is_active=True`.
- **“Token has wrong type”** → only **access** tokens go in `Authorization: Bearer ...`; use **refresh** only at `/token/refresh/`.
- **Can’t create via Swagger** → ensure you clicked **Authorize** and used a token with sufficient permissions (Org Admin or SaaS Admin).

---

## Common variants you can enable

- **Strict RBAC**: remove the `is_org_admin` boolean and enforce “Org Admin” via `Role/UserRole` only (permission class + role seeding).  
- **Email-first login**: token view accepts `email` directly (small serializer override).  
- **Team membership**: add `TeamMembership(user, team, role_in_team)`.  
- **Account Admin**: a role that manages multiple orgs under the same account but not system-wide.  
- **Policy engine**: consume `role.permissions` strings for fine-grained checks.
