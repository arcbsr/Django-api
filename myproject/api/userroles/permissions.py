# myapp/permissions.py

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to users with the 'staff' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'staff'

class IsUserOnly(permissions.BasePermission):
    """
    Allows access only to users with the 'staff' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'



class IsAdminOrStaffUser(permissions.BasePermission):
    """
    Allows access to users with the 'admin' or 'staff' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'staff')
