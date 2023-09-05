from rest_framework import permissions, viewsets

from post.models import Post
from post.permission import DeletePostPermission
from post.serializers import CreatePostSerializer, PostSerializer


class UserPostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, DeletePostPermission]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CreatePostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return (
            Post.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by(
                "-created_at",
            )
        )


class MainPostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related("user").all().order_by("-created_at")
