from django.urls import include, path

urlpatterns = [
    path("auth/", include("user.auth.urls")),
    path("profile/", include("user.profile.urls")),
]
