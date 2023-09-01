from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_created=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    Updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(CreatedAtMixin, UpdatedAtMixin):
    id = models.UUIDField(primary_key=True)

    class Meta:
        abstract = True
