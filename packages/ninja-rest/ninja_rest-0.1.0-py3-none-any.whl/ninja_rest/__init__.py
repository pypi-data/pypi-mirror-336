"""
Django Ninja REST - DRF-like features for Django Ninja
"""

__version__ = "0.1.0"

from .schemas import NinjaModelSchema
from .viewsets import NinjaViewSet
from .pagination import PageNumberPagination
from .permissions import IsAuthenticated, AllowAny
from .authentication import AuthenticationMixin
from .mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)
from .generics import (
    GenericAPIView, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
)

__all__ = [
    # Core components
    'NinjaModelSchema',
    'NinjaViewSet',
    'PageNumberPagination',
    'IsAuthenticated',
    'AllowAny',
    'AuthenticationMixin',
    
    # Mixins
    'ListModelMixin',
    'CreateModelMixin',
    'RetrieveModelMixin',
    'UpdateModelMixin',
    'DestroyModelMixin',
    
    # Generic Views
    'GenericAPIView',
    'GenericViewSet',
    'ReadOnlyModelViewSet',
    'ModelViewSet',
]
