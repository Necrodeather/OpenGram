from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedAtModelMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date on created"),
    )

    class Meta:
        abstract = True


class UpdatedAtModelMixin(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date on updated"),
    )

    class Meta:
        abstract = True
