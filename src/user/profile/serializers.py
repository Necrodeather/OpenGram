from rest_framework import serializers

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(read_only=True)
    following = serializers.IntegerField(read_only=True)

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
        read_only_fields = ["id", "date_joined"]


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["avatar"]
