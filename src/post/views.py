from rest_framework import permissions, generics, viewsets, status

from post.models import Post
from post.serializer import CreatePostSerializer, PostSerializer


class PostView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
    viewsets.ViewSet,
):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostSerializer
        if self.action in ("create", "update", "partial_update"):
            return CreatePostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Post.objects.all()

    def perform_destroy(self, instance):
        if not instance.user != self.request.user:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        instance.delete()
