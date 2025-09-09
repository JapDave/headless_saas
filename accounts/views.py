from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Account, Organization
from .serializers import AccountSerializer, OrganizationSerializer
from users.permissions import IsSaaSAdmin, IsSelfOrganizationOrSaaS

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsSaaSAdmin]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    SaaS Admin: list/create/update/destroy
    Any user: retrieve only their own org (by pk)
    """
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        qs = Organization.objects.select_related("account").all()
        user = self.request.user
        if user.is_staff:
            # support nested list under account
            account_id = self.kwargs.get("account_pk")
            return qs.filter(account_id=account_id) if account_id else qs
        # non-staff: never list; restrict to own org for retrieve/update/delete
        if self.action == "list":
            return qs.none()
        return qs.filter(pk=getattr(user, "organization_id", None))

    def get_permissions(self):
        if self.action in ["list", "create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSaaSAdmin()]
        # retrieve should allow only self org (or SaaS)
        return [IsAuthenticated(), IsSelfOrganizationOrSaaS()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if "accountId" not in data and "account_pk" in self.kwargs:
            data["accountId"] = int(self.kwargs["account_pk"])
        s = self.get_serializer(data=data); s.is_valid(raise_exception=True)
        self.perform_create(s)
        return Response(s.data, status=status.HTTP_201_CREATED)
