from django.urls import path

from user.profile.views import (
    SelfProfileAvatarView,
    SelfProfileView,
    SubscribersView,
    UserProfileView,
)

urlpatterns = [
    path("self/", SelfProfileView.as_view(), name="user-profile"),
    path("avatar/", SelfProfileAvatarView.as_view(), name="user-avatar"),
    path("<str:username>", UserProfileView.as_view(), name="user-profile"),
    path(
        "subscribers/<uuid:user_id>",
        SubscribersView.as_view(),
        name="user-subscribers",
    ),
]
