from core.serializers import OrganizationScopeMixin
from rest_framework import serializers
from accounts.models import Organization
from .models import Role

class RoleSerializer(OrganizationScopeMixin, serializers.ModelSerializer):
    roleId        = serializers.IntegerField(source="id", read_only=True)
    organizationId = serializers.PrimaryKeyRelatedField(source="organization", queryset=Organization.objects.all(), allow_null=True, required=False)
    isCustom      = serializers.BooleanField(source="is_custom", required=False)
    permissions   = serializers.ListField(child=serializers.CharField(), required=False)

    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    deletedAt = serializers.DateTimeField(source="deleted_at", read_only=True)

    class Meta:
        model = Role
        fields = [
            "roleId", "organizationId", "name", "description", "isCustom",
            "permissions", "createdAt", "updatedAt", "deletedAt"
        ]
