from typing import Any, Dict, Generic, Optional, Type, TypeVar
from django.db.models import Model, QuerySet
from django.http import Http404
from ninja import Router, Schema
from .mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)
ListSchemaType = TypeVar("ListSchemaType", bound=Schema)
DetailSchemaType = TypeVar("DetailSchemaType", bound=Schema)

class GenericAPIView(Generic[ModelType]):
    """
    Base class for all generic API views.
    """
    queryset: Optional[QuerySet] = None
    lookup_field: str = 'pk'
    schema: Optional[Type[Schema]] = None
    pagination_class: Optional[Type] = None

    def get_queryset(self) -> QuerySet:
        """
        Get the base queryset for the view.
        Override this method to customize the queryset.
        """
        assert self.queryset is not None, (
            f"'{self.__class__.__name__}' should include a `queryset` attribute "
            "or override the `get_queryset()` method."
        )
        return self.queryset

    def get_object(self, id: Any) -> ModelType:
        """
        Get a single object from the queryset.
        """
        try:
            return self.get_queryset().get(**{self.lookup_field: id})
        except Model.DoesNotExist:
            raise Http404

    def paginate_queryset(self, queryset: QuerySet) -> Dict[str, Any]:
        """
        Paginate the queryset if pagination is enabled.
        """
        if not self.pagination_class:
            return list(queryset)
        
        paginator = self.pagination_class()
        return paginator.paginate_queryset(queryset, self.request)

class GenericViewSet(GenericAPIView):
    """
    The GenericViewSet class does not include any actions by default.
    """
    @classmethod
    def register(cls, router: Router, prefix: str) -> None:
        """
        Register the viewset with a router.
        Override this method to customize URL registration.
        """
        instance = cls()
        
        # Register available actions
        if hasattr(instance, 'list'):
            router.add_api_operation(f"/{prefix}", "GET", instance.list)
        
        if hasattr(instance, 'create'):
            router.add_api_operation(f"/{prefix}", "POST", instance.create)
        
        if hasattr(instance, 'retrieve'):
            router.add_api_operation(f"/{prefix}/{{id}}", "GET", instance.retrieve)
        
        if hasattr(instance, 'update'):
            router.add_api_operation(f"/{prefix}/{{id}}", "PUT", instance.update)
        
        if hasattr(instance, 'destroy'):
            router.add_api_operation(f"/{prefix}/{{id}}", "DELETE", instance.destroy)

class ReadOnlyModelViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
    Generic[ModelType, ListSchemaType, DetailSchemaType]
):
    """
    A viewset that provides default 'read-only' actions:
    - list
    - retrieve
    """
    pass

class ModelViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ListSchemaType, DetailSchemaType]
):
    """
    A viewset that provides default CRUD actions:
    - create
    - list
    - retrieve
    - update
    - destroy
    """
    pass
