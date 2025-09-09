from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Role
from .serializers import RoleSerializer
from users.permissions import IsSameOrgOrSaaSAdmin, IsOrgAdminRoleOrSaaS
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    """
    /organizations/{org_pk}/roles/
    - Read: same org or SaaS  (set stricter policy below if desired)
    - Write: Org Admin or SaaS
    """
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(organization_id=self.kwargs.get("org_pk"))

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSameOrgOrSaaSAdmin(), IsOrgAdminRoleOrSaaS()]
        return [IsAuthenticated(), IsSameOrgOrSaaSAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # inject org from the URL so the serializer validates
        data.setdefault("organizationId", int(self.kwargs["org_pk"]))
        s = self.get_serializer(data=data)
        s.is_valid(raise_exception=True)
        self.perform_create(s)
        return Response(s.data, status=status.HTTP_201_CREATED)