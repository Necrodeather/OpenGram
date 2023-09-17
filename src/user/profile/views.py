from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from common.permission import UserPermission
from user.models import CustomUser, Subscribers
from user.profile.serializers import UserAvatarSerializer, UserSerializer


@extend_schema(tags=["self"])
class SelfProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=["self"])
class SelfProfileAvatarView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = UserAvatarSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=["profile"])
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self):
        return CustomUser.objects.filter(
            username=self.kwargs.get(self.lookup_field),
        )


@extend_schema(tags=["subscribers"])
class SubscribersView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, UserPermission]
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self):
        return CustomUser.objects.prefetch_related("subscribers").filter(
            subscribers__followers__user__username=self.kwargs.get(
                self.lookup_field,
            ),
        )

    def create(self, request, *args, **kwargs):
        profile = get_object_or_404(
            CustomUser,
            username=kwargs.get(self.lookup_field),
        )
        if profile.username == request.user.username:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        following = Subscribers.objects.create(user=profile)
        follower = Subscribers.objects.create(user=request.user)
        following.followers.add(follower)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        profile = get_object_or_404(
            Subscribers,
            user__username=kwargs.get(self.lookup_field),
        )
        follower = get_object_or_404(
            Subscribers,
            user=request.user,
        )
        profile.followers.remove(follower)
        return Response(status=status.HTTP_204_NO_CONTENT)
