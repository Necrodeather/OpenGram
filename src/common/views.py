from rest_framework import generics, permissions

from common.permission import UserPermission


class ListCreateDestroyView(
    generics.ListCreateAPIView,
    generics.DestroyAPIView,
):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
