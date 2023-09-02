from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel


class CustomUser(AbstractBaseUser, BaseModel, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        verbose_name=_("Username"),
        unique=True,
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("First Name"),
        null=True,
        blank=True,
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name=_("Middle Name"),
        null=True,
        blank=True,
    )
    second_name = models.CharField(
        max_length=50,
        verbose_name=_("Second Name"),
        null=True,
        blank=True,
    )
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    phone = PhoneNumberField(
        verbose_name=_("Phone"),
        unique=True,
        null=True,
        blank=True,
    )
    about_me = models.TextField(
        verbose_name=_("About me"),
        default="",
        blank=True,
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=36,
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name=_("Birthday"),
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
