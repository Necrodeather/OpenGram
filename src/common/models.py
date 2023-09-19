from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        verbose_name=_("identifier"),
    )

    class Meta:
        abstract = True
