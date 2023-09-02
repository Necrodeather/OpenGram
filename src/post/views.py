from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from post.serializer import PostSerializer


class CreatePostView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer


class ListPostView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
