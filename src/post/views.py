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
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all().order_by("-created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(post=post, user=self.request.user)
        post.comment = post.comment + 1
        post.save()

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        instance.delete()
        post.comment = post.comment - 1 if post.comment < 0 else 0
        post.save()


@extend_schema(tags=["comment"])
class CommentLikesView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = LikeSerializer
    lookup_field = "comment_id"

    def get_queryset(self):
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs.get(self.lookup_field),
            post_id=self.kwargs.get("post_id"),
        )
        return comment.comment_likes.all().order_by("-created_at")

    def perform_create(self, serializer):
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs.get("id"),
            post_id=self.kwargs.get("post_id"),
        )
        obj, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=self.request.user,
        )
        if not created:
            return
        comment.like = comment.like + 1
        comment.save()

    def perform_destroy(self, instance):
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs.get(self.lookup_field),
            post_id=self.kwargs.get("post_id"),
        )
        if comment.like == 0:
            return
        instance.delete()
        comment.like = comment.like - 1
        comment.save()


@extend_schema(tags=["post"])
class PostLikesView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = LikeSerializer
    lookup_field = "id"

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get(self.lookup_field),
        )
        return post.post_likes.all().order_by("-created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get(self.lookup_field),
        )
        obj, created = PostLike.objects.get_or_create(
            post=post,
            user=self.request.user,
        )
        if not created:
            return
        post.like = post.like + 1
        post.save()

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=self.kwargs.get(self.lookup_field),
        )
        post_like = get_object_or_404(
            PostLike,
            post=post,
            user=self.request.user,
        )
        post_like.delete()
        post.like = post.like - 1
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
