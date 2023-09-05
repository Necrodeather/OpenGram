from django.urls import path

from user.profile.views import ProfileAvatarView, ProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("avatar/", ProfileAvatarView.as_view(), name="avatar"),
]
