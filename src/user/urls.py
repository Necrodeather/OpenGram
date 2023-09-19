from django.urls import include, path

urlpatterns = [
    path("auth/", include("user.auth.urls"), name="authorization"),
    path("profile/", include("user.profile.urls"), name="profile"),
]
