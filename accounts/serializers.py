from rest_framework import serializers
from .models import Account, Organization

class AccountSerializer(serializers.ModelSerializer):
    # IDs & audit timestamps (camelCase)
    accountId  = serializers.IntegerField(source="id", read_only=True)
    contactEmail = serializers.EmailField(source="contact_email", allow_null=True, required=False)
    isActive   = serializers.BooleanField(source="is_active", required=False)
    createdBy  = serializers.IntegerField(source="created_by_id", read_only=True)
    createdAt  = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt  = serializers.DateTimeField(source="updated_at", read_only=True)
    deletedAt  = serializers.DateTimeField(source="deleted_at", read_only=True)

    class Meta:
        model = Account
        # Only camelCase (and spec) fields exposed
        fields = [
            "accountId", "name", "description", "contactEmail", "isActive",
            "createdBy", "createdAt", "updatedAt", "deletedAt"
        ]

class OrganizationSerializer(serializers.ModelSerializer):
    organizationId = serializers.IntegerField(source="id", read_only=True)
    # PK relation as camelCase; this will accept an integer and also render the pk
    accountId = serializers.PrimaryKeyRelatedField(source="account", queryset=Account.objects.all())
    logoUrl   = serializers.URLField(source="logo_url", required=False, allow_blank=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    deletedAt = serializers.DateTimeField(source="deleted_at", read_only=True)

    class Meta:
        model = Organization
        fields = [
            "organizationId", "accountId", "name", "description", "logoUrl",
            "createdAt", "updatedAt", "deletedAt"
        ]
    