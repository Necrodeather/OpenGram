from rest_framework import serializers

from user.models import CustomUser


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ForgotPasswordOrRetryConfrimSerializer(serializers.Serializer):
    login = serializers.CharField(write_only=True)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
