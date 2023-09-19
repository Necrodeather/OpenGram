from rest_framework import serializers

from user.models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
