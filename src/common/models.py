from django.db import models

import uuid


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    Updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(CreatedAtMixin, UpdatedAtMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)

    class Meta:
        abstract = True
