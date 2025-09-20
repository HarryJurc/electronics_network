from rest_framework.permissions import BasePermission

class IsActiveStaff(BasePermission):
    """
    Позволяет доступ только активным сотрудникам (is_staff=True, is_active=True).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff and
            request.user.is_active
        )
