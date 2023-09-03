from django.urls import include, path

from rest_framework import routers

from user.profile.views import UserView

router = routers.DefaultRouter()
router.register(r"", UserView, basename="profile")


urlpatterns = [path("", include(router.urls))]
