from drf_spectacular.utils import extend_schema
from rest_framework import generics, parsers, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from common.permission import UserPermission
from post.models import Comment, CommentLike, Post, PostLike
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
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return (
            Comment.objects.select_related("post")
            .filter(post_id=self.kwargs.get("post_id"))
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(post=post, user=self.request.user)
        post.comment = post.comment + 1
        post.save()

    def perform_destroy(self, instance):
        instance.post.comment = instance.post.comment - 1
        instance.post.save()
        instance.delete()


@extend_schema(tags=["comment"])
class CommentLikesView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = LikeSerializer
    lookup_field = "comment_id"

    def get_queryset(self):
        return (
            CommentLike.objects.select_related("comment")
            .filter(comment_id=self.kwargs.get(self.lookup_field))
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        obj, created = CommentLike.objects.get_or_create(
            comment_id=kwargs.get(self.lookup_field),
            user=request.user,
        )
        if not created:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        obj.comment.like = obj.comment.like + 1
        obj.comment.save()
        return Response(status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.comment.like = instance.comment.like - 1
        instance.comment.save()
        instance.delete()


@extend_schema(tags=["post"])
class PostLikesView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = LikeSerializer
    lookup_field = "id"

    def get_queryset(self):
        return (
            PostLike.objects.select_related("post")
            .filter(post_id=self.kwargs.get(self.lookup_field))
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        obj, created = PostLike.objects.get_or_create(
            post_id=kwargs.get(self.lookup_field),
            user=request.user,
        )
        if not created:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        obj.post.like = obj.post.like + 1
        obj.post.save()
        return Response(status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.post.like = instance.post.like - 1
        instance.post.save()
        instance.delete()
