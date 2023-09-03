from rest_framework.permissions import BasePermission


class DeletePostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.user == request.user
        return True
