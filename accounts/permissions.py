from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Admin can do everything.
    Authenticated users can only read.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.is_staff