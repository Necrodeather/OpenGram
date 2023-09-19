from uuid import uuid4

from rest_framework import serializers

from post.models import Comment, Image, Post
from user.models import CustomUser


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class UpdateSelfPostSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(
        child=ImagePostSerializer(),
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ["id", "description", "images"]
        extra_kwargs = {"id": {"read_only": True}}


class CreateSelfPostSerializer(serializers.ModelSerializer):
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
    )
    images = serializers.ListSerializer(
        child=ImagePostSerializer(),
        read_only=True,
    )

    def create(self, validated_data):
        post = Post.objects.create(
            description=validated_data["description"],
            user=validated_data["user"],
        )
        images = []
        for image in validated_data["upload_images"]:
            image.name = str(uuid4())
            images.append(Image(post=post, image=image))
        post.images.bulk_create(images, batch_size=10)
        return post

    class Meta:
        model = Post
        fields = ["id", "upload_images", "description", "images"]
        extra_kwargs = {"id": {"read_only": True}}


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class PostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    images = serializers.ListSerializer(
        child=ImagePostSerializer(),
    )
    comment = serializers.IntegerField(read_only=True)
    like = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "images",
            "description",
            "created_at",
            "comment",
            "like",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True)
    like = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "parent_id", "text", "like"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "parent_id": {"allow_null": True},
        }


class LikeSerializer(serializers.Serializer):
    user = UserPostSerializer(read_only=True)
