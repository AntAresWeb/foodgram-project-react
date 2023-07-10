from rest_framework import permissions


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Аутентифицированный пользователь (user) — может: читать всё; публиковать
    отзывы и ставить оценки произведениям (фильмам/книгам/песенкам);
    комментировать отзывы; редактировать и удалять свои отзывы
    и комментарии; редактировать свои оценки произведений."""

    message = "Отсутствует доступ на изменение и удаление чужого контента"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Модератор (moderator) — те же права, что и у Аутентифицированного
    пользователя, плюс право удалять и редактировать любые отзывы и
    комментарии."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user or request.user.is_authenticated
                and request.user.role == 'moderator')


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор (admin) — имеет полные права на управление всем контентом
    проекта. Может: создавать и удалять произведения, категории и жанры;
    назначать роли пользователям."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """Суперюзер Django всегда обладает правами администратора, пользователя с
    правами admin. Даже если изменить пользовательскую роль суперюзера — это не
    лишит его прав администратора."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
