from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Team
from .serializers import TeamSerializer
from users.permissions import IsSameOrgOrSaaSAdmin, IsOrgAdminRoleOrSaaS

class TeamViewSet(viewsets.ModelViewSet):
    """
    /organizations/{org_pk}/teams/
    - Read: same org or SaaS
    - Write: Org Admin or SaaS
    """
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.filter(organization_id=self.kwargs.get("org_pk"))

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSameOrgOrSaaSAdmin(), IsOrgAdminRoleOrSaaS()]
        return [IsAuthenticated(), IsSameOrgOrSaaSAdmin()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if "organizationId" not in data:
            data["organizationId"] = int(self.kwargs["org_pk"])
        s = self.get_serializer(data=data); s.is_valid(raise_exception=True)
        self.perform_create(s)
        return Response(s.data, status=status.HTTP_201_CREATED)
