from rest_framework import permissions


class IsAuthenOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CustomIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def authenticate_header(self, request):
        return 'Bearer realm="api"'