from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from common.mixins import CreatedAtModelMixin
from common.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
    avatar = models.ImageField(
        upload_to="static/avatars",
        verbose_name=_("avatar"),
        blank=True,
        null=True,
    )
    middle_name = models.CharField(
        max_length=150,
        verbose_name=_("middle Name"),
        blank=True,
        null=True,
    )
    email = models.EmailField(verbose_name=_("email"), unique=True)
    phone = PhoneNumberField(
        verbose_name=_("phone"),
        unique=True,
        null=True,
        blank=True,
    )
    following = models.IntegerField(
        verbose_name=_("following"),
        default=0,
    )
    followers = models.IntegerField(
        verbose_name=_("followers"),
        default=0,
    )
    about_me = models.TextField(
        verbose_name=_("about me"),
        default="",
        blank=True,
    )
    city = models.CharField(
        verbose_name=_("city"),
        max_length=36,
        blank=True,
        null=True,
    )
    birthday = models.DateField(
        verbose_name=_("birthday"),
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        _("active"),
        default=False,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Subscribers(BaseModel, CreatedAtModelMixin):
    user = models.OneToOneField(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name=_("user"),
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        verbose_name=_("followers"),
    )

    class Meta:
        verbose_name = _("subscriber")
        verbose_name_plural = _("subscribers")

    def __str__(self):
        return self.user.username
