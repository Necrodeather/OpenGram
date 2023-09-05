from rest_framework import serializers

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "is_superuser",
            "password",
            "last_login",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "date_joined": {"read_only": True},
        }


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["avatar"]
