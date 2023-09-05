from rest_framework import serializers

from post.models import Post
from user.models import CustomUser


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["media", "description"]


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "media",
            "description",
            "like",
            "comment",
            "created_at",
        ]
