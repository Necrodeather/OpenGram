from django.contrib.auth.hashers import make_password
from django.core.cache import cache

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.auth.serializers import CreateUserSerializer
from user.auth.task import send_confirmation_email
from user.models import CustomUser


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.initial_data["password"]),
        )
        send_confirmation_email.delay(serializer.data)


class ConfirmRegistration(APIView):
    serializer_class = CreateUserSerializer

    def get(self, request, token):
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
