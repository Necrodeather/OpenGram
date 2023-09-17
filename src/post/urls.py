from django.urls import include, path

from rest_framework import routers

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
    path("", include(router.urls), name="self-posts"),
    path(
        "user-posts/<uuid:user_id>",
        UserPostsView.as_view(),
        name="user-posts",
    ),
    path(
        "comments/<uuid:post_id>/<uuid:comment_id>/likes",
        CommentLikesView.as_view(),
        name="comment-likes",
    ),
    path(
        "post-likes/<uuid:id>",
        PostLikesView.as_view(),
        name="post-likes",
    ),
]
