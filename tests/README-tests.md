# Running the test suite

## Docker (recommended)
```bash
docker compose exec web pytest -q
# verbose & stop on first failure
docker compose exec web pytest -vv -x
```

## Local (venv)
```bash
pytest -q
```

### Notes
- Tests obtain JWTs via `/api/auth/token/` then call endpoints with `Authorization: Bearer <access>`.
- The suite assumes the permission policy:
  - Accounts: SaaS-only.
  - Organizations: SaaS full CRUD; others can only retrieve **their** org.
  - Org-scoped (Users/Teams/Roles/Subscriptions): read same-org; write requires Org Admin.
- If Roles must be hidden from Members, change `test_roles.py::test_roles_list_same_org_visibility` to assert `403`.
