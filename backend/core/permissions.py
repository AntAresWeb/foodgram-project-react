from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import (
                BlacklistedToken, OutstandingToken, RefreshToken)
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
#        user, token = JWTAuthentication().authenticate(request)
        is_allowed_user = True
        token = str(request.auth)
        try:
            is_blacklisted = BlacklistedToken.objects.filter(token__token=token)
            print('--->>>', is_blacklisted)
            is_whitelisted = OutstandingToken.objects.filter(token=token)
            print('--->>>', is_whitelisted)
            if is_blacklisted:
                is_allowed_user = False
        except BlacklistedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
