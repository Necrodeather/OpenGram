from django.contrib.auth.hashers import make_password

from rest_framework import generics

from user.auth.serializers import CreateUserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.initial_data["password"]),
        )
