from rest_framework import generics, permissions, viewsets

from post.models import Post
from post.permission import DeletePostPermission
from post.serializer import CreatePostSerializer, PostSerializer


class PostView(
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
        return Post.objects.all()
