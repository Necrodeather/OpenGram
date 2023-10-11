from drf_spectacular.utils import extend_schema
from rest_framework import generics, parsers, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from common.permission import UserPermission
from common.views import ListCreateDestroyView
from post.models import Comment, Like, Post
from post.serializers import (
    CommentSerializer,
    CreateSelfPostSerializer,
    LikeSerializer,
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
        return UpdateSelfPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


@extend_schema(tags=["post"])
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user__username=self.kwargs.get("username"))


@extend_schema(tags=["comment"])
class CommentPostView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        serializer.save(
            post=get_object_or_404(Post, pk=self.kwargs.get("post_id")),
            user=self.request.user,
        )


@extend_schema(tags=["comment"])
class CommentLikesView(ListCreateDestroyView):
    serializer_class = LikeSerializer
    lookup_field = "comment_id"

    def get_queryset(self):
        return Like.objects.select_related("comment").filter(
            comment_id=self.kwargs.get(self.lookup_field),
        )

    def create(self, request, *args, **kwargs):
        obj, created = Like.objects.get_or_create(
            comment_id=kwargs.get(self.lookup_field),
            user=request.user,
        )
        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


@extend_schema(tags=["post"])
class PostLikesView(ListCreateDestroyView):
    serializer_class = LikeSerializer
    lookup_field = "post_id"

    def get_queryset(self):
        return Like.objects.select_related("post").filter(
            post_id=self.kwargs.get(self.lookup_field),
        )

    def create(self, request, *args, **kwargs):
        obj, created = Like.objects.get_or_create(
            post_id=kwargs.get(self.lookup_field),
            user=request.user,
        )
        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
