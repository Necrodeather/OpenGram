from rest_framework import generics, permissions, viewsets

from post.models import Post
from post.permission import DeletePostPermission
from post.serializers import CreatePostSerializer, PostSerializer


class UserPostView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
    viewsets.ViewSet,
):
    permission_classes = [permissions.IsAuthenticated, DeletePostPermission]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CreatePostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by(
            "-created_at",
        )


class MainPostView(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    viewsets.ViewSet,
):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")
