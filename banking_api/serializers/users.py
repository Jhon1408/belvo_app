from rest_framework import serializers
from banking_api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """Defines user serializer behaviour."""

    class Meta:
        """Defines serializer fields that are being used"""

        model = User
        fields = [
            "username",
            "email",
            "is_active",
            "role",
        ]

        extra_kwargs = {"password": {"write_only": True}}
