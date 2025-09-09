from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from users.permissions import IsSameOrgOrSaaSAdmin, IsOrgAdminRoleOrSaaS

class OrgUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(organization_id=self.kwargs.get("org_pk"))

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSameOrgOrSaaSAdmin(), IsOrgAdminRoleOrSaaS()]
        return [IsAuthenticated(), IsSameOrgOrSaaSAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.setdefault("organizationId", int(self.kwargs["org_pk"]))
        s = self.get_serializer(data=data); s.is_valid(raise_exception=True)
        s.save(created_by=request.user)
        return Response(s.data, status=status.HTTP_201_CREATED)
