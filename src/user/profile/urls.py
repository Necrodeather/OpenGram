from django.urls import path

from user.profile.views import ProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
]
