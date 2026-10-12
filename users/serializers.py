from core.serializers import OrganizationScopeMixin
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Organization
from .models import User

class UserSerializer(OrganizationScopeMixin, serializers.ModelSerializer):
    userId         = serializers.IntegerField(source="id", read_only=True)
    organizationId = serializers.PrimaryKeyRelatedField(source="organization", queryset=Organization.objects.all(), allow_null=True, required=False)
    fullName       = serializers.CharField(source="full_name", required=False, allow_blank=True)
    profileImage   = serializers.URLField(source="profile_image", required=False, allow_blank=True)
    userPreferences = serializers.JSONField(source="user_preferences", required=False)
    createdBy      = serializers.IntegerField(source="created_by_id", read_only=True)
    createdAt      = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt      = serializers.DateTimeField(source="updated_at", read_only=True)
    deletedAt      = serializers.DateTimeField(source="deleted_at", read_only=True)

    # Not in spec but useful; keep write-only to support login or set automatically
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "userId", "organizationId", "fullName", "email", "status",
            "profileImage", "userPreferences", "createdBy",
            "createdAt", "updatedAt", "deletedAt", "password"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # If API didn’t send username (not in spec), derive from email for Django
        username = validated_data.get("username")
        if not username:
            email = validated_data.get("email")
            if email:
                validated_data["username"] = email
            else:
                # fallback: generate something
                validated_data["username"] = f"user_{User.objects.count()+1}"

        user = User(**validated_data)
        if password:
            validate_password(password, user=user)
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            validate_password(password, user=instance)
            instance.set_password(password)
        instance.save()
        return instance
