from django.urls import path

from user.profile.views import (
    SelfProfileAvatarView,
    SelfProfileView,
    UserProfileView,
)

urlpatterns = [
    path("self/", SelfProfileView.as_view(), name="user-profile"),
    path("avatar/", SelfProfileAvatarView.as_view(), name="user-avatar"),
    path("<uuid:id>", UserProfileView.as_view(), name="user-profile"),
]
