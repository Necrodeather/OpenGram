from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.auth.views import (
    ConfirmRegistrationView,
    CreateUserView,
    ForgotPasswordView,
    SetPasswordView,
    RetryConfirmUser,
)

urlpatterns = [
    path("sign-up/", CreateUserView.as_view(), name="register"),
    path("sigh-in/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify"),
    path(
        "confirm-email/<uuid:token>",
        ConfirmRegistrationView.as_view(),
        name="confirm-email",
    ),
    path(
        "forgot-password",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "reset-password/<uuid:token>",
        SetPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "retry-confirm-user",
        RetryConfirmUser.as_view(),
        name="retry_confirm_user",
    ),
]
