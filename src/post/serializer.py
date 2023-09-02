from rest_framework import serializers

from post.models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["media", "description"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "user",
            "media",
            "description",
            "like",
            "comment",
            "created_at",
        ]
