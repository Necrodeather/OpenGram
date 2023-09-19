from django.db import models
from django.utils.translation import gettext_lazy as _

from common.mixins import CreatedAtModelMixin, UpdatedAtModelMixin
from common.models import BaseModel
from post.managers import CustomCommentManager, CustomPostManager


class Post(BaseModel, CreatedAtModelMixin, UpdatedAtModelMixin):
    description = models.TextField(
        verbose_name=_("description"),
        default="",
        blank=True,
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("user"),
    )

    objects = CustomPostManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")


class Image(BaseModel, CreatedAtModelMixin):
    image = models.ImageField(
        upload_to="static/post",
        verbose_name=_("image"),
    )
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class Like(BaseModel, CreatedAtModelMixin):
    comment = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("comment"),
        null=True,
    )
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("post"),
        null=True,
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
        verbose_name = _("like")
        verbose_name_plural = _("likes")


class Comment(BaseModel, CreatedAtModelMixin, UpdatedAtModelMixin):
    text = models.TextField(verbose_name=_("text"))
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

    objects = CustomCommentManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
