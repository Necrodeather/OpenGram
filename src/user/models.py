from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
