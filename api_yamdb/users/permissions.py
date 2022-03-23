from rest_framework import permissions


class ContentModificationPermission(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_superuser
                or request.user.is_moderator()
                or request.user.is_admin())


class AdminPermission(permissions.BasePermission):
    message = 'Для доступа необходимы права администратора.'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and request.user.is_admin())


class ModeratorPermission(permissions.BasePermission):
    message = 'Для доступа необходимы права модератора.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_staff
                or request.user.is_moderator())
