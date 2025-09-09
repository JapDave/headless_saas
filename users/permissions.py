from rest_framework.permissions import BasePermission
from typing import Optional

def _kw(view, *names) -> Optional[str]:
    for n in names:
        if n in view.kwargs:
            return str(view.kwargs[n])
    return None

class IsSaaSAdmin(BasePermission):
    """System admin: Django is_staff."""
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.is_staff)

class IsSameOrgOrSaaSAdmin(BasePermission):
    """
    For org-scoped routes like /organizations/{org_pk}/... .
    Allows if user's organization == org_pk or user is SaaS admin.
    """
    def has_permission(self, request, view):
        u = request.user
        if not (u and u.is_authenticated):
            return False
        if u.is_staff:
            return True
        org_pk = _kw(view, "org_pk")  # org-scoped routes
        return org_pk is not None and str(getattr(u, "organization_id", None)) == org_pk

class IsSelfOrganizationOrSaaS(BasePermission):
    """
    For organization DETAIL route where org id is path 'pk':
    /api/accounts/{account_pk}/organizations/{pk}/
    """
    def has_permission(self, request, view):
        u = request.user
        if not (u and u.is_authenticated):
            return False
        if u.is_staff:
            return True
        org_id = _kw(view, "pk")  # organization detail uses 'pk'
        return org_id is not None and str(getattr(u, "organization_id", None)) == org_id

class IsOrgAdminRoleOrSaaS(BasePermission):
    """Require Org Admin in this org (or SaaS Admin)."""
    def has_permission(self, request, view):
        u = request.user
        if not (u and u.is_authenticated):
            return False
        if u.is_staff:
            return True
        # Accept org id from either org-scoped routes or org detail
        org_id = _kw(view, "org_pk", "pk")
        if org_id is None:
            return False
        # If you kept a boolean flag:
        if getattr(u, "is_org_admin", False) and str(getattr(u, "organization_id", None)) == org_id:
            return True
        from roles.models import UserRole
        return UserRole.objects.filter(
            user=u, role__organization_id=org_id, role__name="Org Admin"
        ).exists()
