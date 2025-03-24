from typing import Any
from django.http import HttpRequest

class BasePermission:
    """
    Base class for all permissions. This class defines the interface that all
    permission classes must implement. The methods in this class are meant to be
    overridden by subclasses.
    """
    def has_permission(self, request: HttpRequest) -> bool:
        """
        Check if permission should be granted.
        
        Args:
            request: The HTTP request to check permissions for
            
        Returns:
            bool: True if permission is granted, False otherwise
            
        Note:
            This is an interface method that should be overridden by subclasses.
            The base implementation returns True to allow permissive behavior by default.
        """
        return True

    def has_object_permission(self, request: HttpRequest, obj: Any) -> bool:
        """
        Check if permission should be granted for a specific object.
        
        Args:
            request: The HTTP request to check permissions for
            obj: The object to check permissions against
            
        Returns:
            bool: True if permission is granted, False otherwise
            
        Note:
            This is an interface method that should be overridden by subclasses.
            The base implementation returns True to allow permissive behavior by default.
        """
        _ = obj  # Acknowledge the parameter even if unused
        return True

class IsAuthenticated(BasePermission):
    """
    Permission class that requires the user to be authenticated
    """
    def has_permission(self, request: HttpRequest) -> bool:
        return bool(request.user and request.user.is_authenticated)

class AllowAny(BasePermission):
    """
    Permission class that allows unrestricted access
    """
    def has_permission(self, request: HttpRequest) -> bool:
        return True

class IsAdminUser(BasePermission):
    """
    Permission class that requires the user to be an admin
    """
    def has_permission(self, request: HttpRequest) -> bool:
        return bool(request.user and request.user.is_staff)

class IsOwner(BasePermission):
    """
    Permission class that requires the user to be the owner of an object
    """
    def has_object_permission(self, request: HttpRequest, obj) -> bool:
        return hasattr(obj, 'user') and obj.user == request.user
