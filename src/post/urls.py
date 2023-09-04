from django.urls import include, path

from rest_framework import routers

from post.views import MainPostView, UserPostView

router = routers.DefaultRouter()
router.register(r"user-posts", UserPostView, basename="user-posts")
router.register(r"posts", MainPostView, basename="posts")


urlpatterns = [
    path("", include(router.urls), name="post"),
]
