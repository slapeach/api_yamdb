from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пермишен для доступа  к изменению контента
       только модераторам или авторам"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Пермишен для доступа  к изменению контента
       только модераторам или авторам"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
        )


class IsUserOrReadOnly(permissions.BasePermission):
    """Пермишен для доступа  к изменению данных пользователя """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsSuperUser(permissions.BasePermission):
    """Пермишен для доступа суперпользователю
    к изменению данных пользователей"""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пермишен для доступа  к изменению контента
       только модераторам или авторам"""

    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.role == 'admin')
