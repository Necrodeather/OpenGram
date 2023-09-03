from rest_framework import generics, permissions, viewsets

from user.profile.serializer import UserSerializer


class UserView(
    generics.RetrieveUpdateAPIView,
    viewsets.ViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
