from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import BlacklistedToken


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
