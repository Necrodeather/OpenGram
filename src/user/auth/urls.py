from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.auth.views import ConfirmRegistration, CreateUserView

urlpatterns = [
    path("sign-up/", CreateUserView.as_view(), name="register"),
    path("sigh-in/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify"),
    path(
        "confirm-email/<uuid:token>",
        ConfirmRegistration.as_view(),
        name="confirm-email",
    ),
]
