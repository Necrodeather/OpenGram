from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.mixins import CreatedAtModelMixin, UpdatedAtModelMixin
from common.models import BaseModel


class Post(BaseModel, CreatedAtModelMixin, UpdatedAtModelMixin):
    class PostTypeChoices(models.TextChoices):
        PHOTO = "Photo", _("photo")
        VIDEO = "Video", _("video")

    type = models.CharField(
        max_length=max([len(post_type) for post_type in PostTypeChoices]),
        choices=PostTypeChoices.choices,
        verbose_name=_("type"),
    )
    media = ArrayField(models.URLField(), verbose_name=_("media"))
    description = models.TextField(
        verbose_name=_("description"),
        default="",
        blank=True,
    )
    like = models.IntegerField(verbose_name=_("like"), default=0)
    comment = models.IntegerField(verbose_name=_("comment"), default=0)
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("user"),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")


class PostLike(BaseModel, CreatedAtModelMixin):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="post_likes",
        verbose_name=_("post"),
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="post_likes",
        verbose_name=_("user"),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("like in post")
        verbose_name_plural = _("likes in posts")


class CommentLike(BaseModel, CreatedAtModelMixin):
    comment = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="comment_likes",
        verbose_name=_("comment"),
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="comment_likes",
        verbose_name=_("user"),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("like in comment")
        verbose_name_plural = _("likes in comments")


class Comment(BaseModel, CreatedAtModelMixin, UpdatedAtModelMixin):
    text = models.TextField(verbose_name=_("text"))
    like = models.IntegerField(verbose_name=_("likes"), default=0)
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("post"),
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("user"),
    )
    parent_id = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
        verbose_name=_("parent comment"),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
