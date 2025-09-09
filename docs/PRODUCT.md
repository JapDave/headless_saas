# Product Document — Headless SaaS API

## Summary
Backend exposes multi-tenant building blocks for a headless SaaS: **Accounts → Organizations → Users/Teams + Subscriptions**.
Includes JWT auth, soft-deletion, pagination, filtering, and auto-generated OpenAPI docs.

## ERD (mermaid)
```mermaid
erDiagram
  Account ||--o{ Organization : contains
  Organization ||--o{ User : has
  Organization ||--o{ Team : has
  Organization ||--o{ Subscription : has
  Role ||--o{ UserRole : assigns
  User ||--o{ UserRole : has
```
