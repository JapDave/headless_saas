# API Cheatsheet

Interactive docs: **/api/docs** (Swagger), **/api/redoc**; schema at **/api/schema**.

## Auth
- `POST /api/auth/token/` (username/password → access, refresh)
- `POST /api/auth/token/refresh/`

## Accounts (SaaS Admin)
- `POST /api/accounts/`, `GET /api/accounts/`, `GET/PUT/PATCH/DELETE /api/accounts/{id}/`
- `GET/POST /api/accounts/{account_id}/organizations/`

## Organizations
- `GET/PUT/PATCH/DELETE /api/accounts/{account_id}/organizations/{id}/`

## Users (org scoped)
- `POST /api/organizations/{org_id}/users/`
- `GET /api/organizations/{org_id}/users/?status=active`
- `GET/PUT/PATCH/DELETE /api/organizations/{org_id}/users/{id}/`

## Teams (org scoped)
- `POST /api/organizations/{org_id}/teams/`
- `GET /api/organizations/{org_id}/teams/`

## Roles (minimal)
- `POST /api/organizations/{org_id}/roles/`
- `GET /api/organizations/{org_id}/roles/`
