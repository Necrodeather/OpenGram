from django.urls import path, include
from rest_framework import routers

from post.views import PostView

router_v1 = routers.DefaultRouter()
router_v1.register(r"post", PostView, basename="post")


urlpatterns = [
    path("", include(router_v1.urls)),
]
