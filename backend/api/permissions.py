from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import BlacklistedToken


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        is_allowed_user = True
        token = str(request.auth)
        try:
            if BlacklistedToken.objects.filter(token__token=token):
                is_allowed_user = False
        except BlacklistedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
