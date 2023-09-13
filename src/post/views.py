from drf_spectacular.utils import extend_schema
from rest_framework import generics, parsers, permissions, viewsets
from rest_framework.generics import get_object_or_404

from post.models import Post
from post.permission import UserPermission
from post.serializers import (
    CommentSerializer,
    CreateSelfPostSerializer,
    PostSerializer,
    UpdateSelfPostSerializer,
)


@extend_schema(tags=["post"])
class SelfPostView(
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    viewsets.ViewSet,
):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    parser_classes = [parsers.MultiPartParser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateSelfPostSerializer
        else:
            return UpdateSelfPostSerializer

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


@extend_schema(tags=["post"])
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Post.objects.select_related("user")
            .filter(**self.kwargs)
            .order_by("-created_at")
        )


@extend_schema(tags=["comment"])
class CommentPostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all().order_by("-created_at")
