from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from user.auth.serializers import (
    AuthUserSerializer,
    ForgotPasswordOrRetryConfrimSerializer,
    SetPasswordSerializer,
)
from user.auth.task import send_confirmation_email, send_reset_password_email
from user.models import CustomUser


class CreateUserView(generics.CreateAPIView):
    serializer_class = AuthUserSerializer

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.initial_data["password"]),
        )

        send_confirmation_email.delay(serializer.data)


class RetryConfirmUser(APIView):
    serializer_class = ForgotPasswordOrRetryConfrimSerializer

    def post(self, request):
        user = get_object_or_404(
            CustomUser,
            Q(email=request.data["login"]) | Q(username=request.data["login"]),
            is_active=False,
        )

        serializer = self.serializer_class(user)
        send_confirmation_email.delay(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ConfirmRegistrationView(APIView):
    serializer_class = AuthUserSerializer

    def post(self, request, token):
        user_cache_data = cache.get(token)
        if not user_cache_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        CustomUser.objects.filter(
            email=user_cache_data["email"],
            is_active=False,
        ).update(is_active=True)

        serializer = self.serializer_class(user_cache_data)
        cache.delete(token)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordOrRetryConfrimSerializer

    def post(self, request):
        user = get_object_or_404(
            CustomUser,
            Q(email=request.data["login"])
            | Q(phone=request.data["login"])
            | Q(username=request.data["login"]),
        )
        serializer = AuthUserSerializer(user)
        send_reset_password_email.delay(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SetPasswordView(APIView):
    serializer_class = SetPasswordSerializer

    def put(self, request, token):
        user_cache_data = cache.get(token)
        if not user_cache_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, email=user_cache_data["email"])
        user.set_password(request.data["password"])

        cache.delete(token)
        return Response(status=status.HTTP_200_OK)
