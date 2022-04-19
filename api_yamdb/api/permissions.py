from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Пермишен для доступа  к изменению контента
       только администратору"""

    def has_permission(self, request, view):
        return request.user.is_staff or (request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.role == 'admin')


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user.role == 'admin')
        )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user == obj.author
                 or request.user.is_staff
                 or (request.user.role == 'admin')
                 or (request.user.role == 'moderator'))
        )
