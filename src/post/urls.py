from django.urls import include, path
from django.views.decorators.cache import cache_page

from rest_framework import routers

from core.settings import CACHE_TTL
from post.views import (
    CommentLikesView,
    CommentPostView,
    PostLikesView,
    SelfPostView,
    UserPostsView,
)

router = routers.DefaultRouter()
router.register("self-posts", SelfPostView, basename="self-posts")
router.register(
    r"comments/(?P<post_id>[\w-]+)",
    CommentPostView,
    basename="post-comments",
)


urlpatterns = [
    path("", cache_page(CACHE_TTL)(include(router.urls)), name="self-posts"),
    path(
        "user-posts/<str:username>",
        cache_page(CACHE_TTL)(UserPostsView.as_view()),
        name="user-posts",
    ),
    path(
        "comments/<uuid:comment_id>/likes",
        cache_page(CACHE_TTL)(CommentLikesView.as_view()),
        name="comment-likes",
    ),
    path(
        "post-likes/<uuid:post_id>",
        cache_page(CACHE_TTL)(PostLikesView.as_view()),
        name="post-likes",
    ),
]
