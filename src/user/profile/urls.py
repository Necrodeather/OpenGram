from django.urls import path
from django.views.decorators.cache import cache_page

from user.profile.views import (
    SelfProfileAvatarView,
    SelfProfileView,
    SubscribersView,
    UserProfileView,
)

urlpatterns = [
    path(
        "self/",
        cache_page(60 * 30)(SelfProfileView.as_view()),
        name="user-profile",
    ),
    path("avatar/", SelfProfileAvatarView.as_view(), name="user-avatar"),
    path(
        "<str:username>",
        cache_page(60 * 30)(UserProfileView.as_view()),
        name="user-profile",
    ),
    path(
        "subscribers/<uuid:user_id>",
        SubscribersView.as_view(),
        name="user-subscribers",
    ),
]
