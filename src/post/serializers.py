from rest_framework import serializers

from post.models import Post
from user.models import CustomUser


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["images", "description"]


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class PostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "images",
            "description",
            "like",
            "comment",
            "created_at",
        ]
