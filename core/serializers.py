from rest_framework import serializers


class OrganizationScopeMixin:
    """Keep nested writes in the organization selected by the URL."""

    def validate(self, attrs):
        attrs = super().validate(attrs)
        org_pk = getattr(self.context.get("view"), "kwargs", {}).get("org_pk")
        if org_pk is not None and "organization" in attrs:
            organization = attrs["organization"]
            if organization is None or organization.pk != int(org_pk):
                raise serializers.ValidationError({"organizationId": "Must match the organization in the URL."})
        return attrs
