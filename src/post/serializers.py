from uuid import uuid4

from rest_framework import serializers

from post.models import Image, Post
from user.models import CustomUser


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class CreatePostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
    )

    def create(self, validated_data):
        post = Post.objects.create(
            description=validated_data["description"],
            user=validated_data["user"],
        )
        images = []
        for image in validated_data["images"]:
            image.name = str(uuid4())
            images.append(Image(post=post, image=image))
        Image.objects.bulk_create(images, batch_size=10)
        post.images = images
        return post

    class Meta:
        model = Post
        fields = ["images", "description"]


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class PostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    images = serializers.ListSerializer(
        child=ImagePostSerializer(),
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
