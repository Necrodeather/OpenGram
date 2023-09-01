from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class Post(BaseModel):
    class PostTypeChoices(models.Choices):
        PHOTO = "Photo"
        VIDEO = "Video"

    type = models.CharField(
        max_length=max([len(post_type.value) for post_type in PostTypeChoices]),
        choices=PostTypeChoices.choices,
        verbose_name=_("Post Type"),
    )
    media = ArrayField(models.URLField(), verbose_name=_("Media"))
    description = models.TextField(
        verbose_name=_("Description"),
        default="",
        blank=True,
    )
    like = models.IntegerField(verbose_name=_("Like"), default=0)
    comment = models.IntegerField(verbose_name=_("Comment"), default=0)
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="posts",
    )

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")


class Like(BaseModel):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


class Comment(BaseModel):
    text = models.TextField()
    like = models.IntegerField()
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    parent_id = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
