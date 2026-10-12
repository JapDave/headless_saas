from core.serializers import OrganizationScopeMixin
from rest_framework import serializers
from accounts.models import Organization
from .models import Team

class TeamSerializer(OrganizationScopeMixin, serializers.ModelSerializer):
    teamId         = serializers.IntegerField(source="id", read_only=True)
    organizationId = serializers.PrimaryKeyRelatedField(source="organization", queryset=Organization.objects.all())
    configurations = serializers.JSONField(required=False)

    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    deletedAt = serializers.DateTimeField(source="deleted_at", read_only=True)

    class Meta:
        model = Team
        fields = [
            "teamId", "organizationId", "name", "description", "configurations",
            "createdAt", "updatedAt", "deletedAt"
        ]
