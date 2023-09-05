from django.contrib import admin

from post.models import Comment, CommentLike, Image, Post, PostLike


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["user__email", "user__username"]
    list_display = ["user", "id", "created_at"]
    exclude = ["id"]


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    search_fields = ["user__email", "user__username"]
    list_display = ["post", "user", "created_at"]
    exclude = ["id"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = [
        "user__email",
        "user__username",
        "post__id",
        "parent_id",
        "id",
    ]
    list_display = ["user", "post", "created_at", "text", "id", "parent_id"]
    exclude = ["id"]


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    search_fields = ["user__email", "user__username"]
    list_display = ["comment", "user", "created_at"]
    exclude = ["id"]
