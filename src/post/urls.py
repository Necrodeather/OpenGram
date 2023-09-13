from django.urls import include, path

from rest_framework import routers

from post.views import CommentPostView, SelfPostView, UserPostsView

router = routers.DefaultRouter()
router.register("self-posts", SelfPostView, basename="self-posts")
router.register(
    r"^comments/(?P<post_id>\d+)",
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
]
