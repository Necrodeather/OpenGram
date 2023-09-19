from django.contrib.auth.models import UserManager
from django.db.models import Count


class CustomUserManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "subscribers__followers",
                "subscribers__following",
            )
            .annotate(
                followers=Count("subscribers__followers__user__id"),
                following=Count("subscribers__following__user__id"),
            )
            .filter(is_active=True)
        )
