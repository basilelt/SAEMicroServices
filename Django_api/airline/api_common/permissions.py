from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers or staff members to delete a flight.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a superuser or staff
        return request.user and request.user.is_staff