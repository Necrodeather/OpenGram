from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ["username", "email", "phone"]
    list_display = ["username", "email", "phone", "last_login", "is_active"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "phone",
                    "city",
                    "birthday",
                    "about_me",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active",),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
