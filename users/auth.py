from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class StatusAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if getattr(user, "status", "active") != "active":
            raise serializers.ValidationError("User is not active (status).")
        return data
