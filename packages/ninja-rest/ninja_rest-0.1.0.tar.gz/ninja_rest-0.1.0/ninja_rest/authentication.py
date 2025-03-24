from typing import Optional
from django.http import HttpRequest
from ninja.security import HttpBearer

class AuthenticationMixin:
    """
    Mixin to add authentication to Django Ninja endpoints
    """
    authentication_classes = []
    permission_classes = []

    def get_authenticators(self):
        """Get list of authenticator instances"""
        return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        """Get list of permission instances"""
        return [permission() for permission in self.permission_classes]

    def check_authentication(self, request: HttpRequest):
        """Check if request is authenticated"""
        for authenticator in self.get_authenticators():
            result = authenticator(request)
            if result:
                request.auth = result
                return True
        return False

    def check_permissions(self, request: HttpRequest):
        """Check if request has required permissions"""
        for permission in self.get_permissions():
            if not permission.has_permission(request):
                return False
        return True

class TokenAuthentication(HttpBearer):
    """
    Token-based authentication using Bearer tokens
    """
    def authenticate(self, request: HttpRequest, token: str) -> Optional[str]:
        # Implement your token validation logic here
        # For example, check against your token model
        try:
            # Example: Token.objects.get(key=token)
            return token
        except Exception:
            return None
