from django.db import models
from django.db.models import Count


class CustomPostManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user")
            .prefetch_related("comments", "likes")
            .annotate(comment=Count("comments__id"), like=Count("likes__id"))
        )


class CustomCommentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("post")
            .prefetch_related("likes")
            .annotate(like=Count("likes__id"))
        )
