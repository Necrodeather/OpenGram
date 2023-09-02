from django.contrib import admin

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ["username", "email"]
    list_display = ["username", "email", "last_login", "is_staff"]
    exclude = ["id", "groups", "is_superuser", "user_permissions", "password"]
