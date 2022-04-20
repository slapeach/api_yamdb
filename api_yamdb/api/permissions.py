from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    """Пермишен для доступа  к изменению контента
       только администратору"""

    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == ADMIN)

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.role == ADMIN)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пермишен для Админа, или только чтение"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_staff)
        )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Пермишен для автора, админа и модератора, или только чтение"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user == obj.author
                 or request.user.is_staff
                 or (request.user.role == ADMIN)
                 or (request.user.role == MODERATOR))
        )
