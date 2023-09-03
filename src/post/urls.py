from django.urls import include, path

from rest_framework import routers

from post.views import PostView

router = routers.DefaultRouter()
router.register(r"post", PostView, basename="post")


urlpatterns = [
    path("", include(router.urls)),
]
