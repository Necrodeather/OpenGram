from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

urlpatterns = [
    path("token/", TokenObtainSlidingView.as_view()),
    path("token/refresh/", TokenRefreshSlidingView.as_view()),
]
