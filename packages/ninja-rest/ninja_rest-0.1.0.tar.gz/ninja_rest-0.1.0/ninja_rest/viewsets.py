from typing import Any, List, Optional, Type
from django.db.models import QuerySet, Model
from django.http import Http404
from ninja import Router
from ninja.pagination import PaginationBase
from .schemas import NinjaModelSchema
from .pagination import PageNumberPagination

class NinjaViewSet:
    """
    A ViewSet class that provides DRF-like functionality for Django Ninja
    """
    schema: Optional[Type[NinjaModelSchema]] = None
    queryset: Optional[QuerySet] = None
    pagination_class: Optional[Type[PaginationBase]] = PageNumberPagination
    lookup_field: str = 'pk'

    @classmethod
    def register(cls, router: Router, prefix: str = None):
        """Register all viewset routes with the router"""
        if not cls.schema:
            raise ValueError("schema must be set")

        if prefix is None:
            prefix = cls.schema.__name__.lower().replace('schema', '')

        # List and Create
        @router.get(f"/{prefix}", response=List[cls.schema])
        def list_items(request, **kwargs):
            instance = cls()
            queryset = instance.get_queryset()
            if instance.pagination_class:
                paginator = instance.pagination_class()
                return paginator.paginate_queryset(queryset, request, **kwargs)
            return list(queryset)

        @router.post(f"/{prefix}", response=cls.schema)
        def create_item(request, payload: cls.schema):
            instance = cls()
            return instance.perform_create(payload)

        # Retrieve, Update, Delete
        @router.get(f"/{prefix}/{{pk}}", response=cls.schema)
        def retrieve_item(request, pk: Any):
            instance = cls()
            return instance.get_object(pk)

        @router.put(f"/{prefix}/{{pk}}", response=cls.schema)
        def update_item(request, pk: Any, payload: cls.schema):
            instance = cls()
            obj = instance.get_object(pk)
            return instance.perform_update(obj, payload)

        @router.delete(f"/{prefix}/{{pk}}", response=None)
        def delete_item(request, pk: Any):
            instance = cls()
            obj = instance.get_object(pk)
            return instance.perform_delete(obj)

    def get_queryset(self) -> QuerySet:
        """Get the base queryset for the viewset"""
        if self.queryset is None:
            if self.schema and hasattr(self.schema.Config, 'model'):
                return self.schema.Config.model.objects.all()
            raise ValueError("Either queryset or schema.Config.model must be set")
        return self.queryset

    def get_object(self, pk: Any) -> Model:
        """Get a single object from the queryset"""
        try:
            return self.get_queryset().get(**{self.lookup_field: pk})
        except Model.DoesNotExist:
            raise Http404

    def perform_create(self, schema_instance: NinjaModelSchema) -> Model:
        """Create a new instance"""
        return schema_instance.create(schema_instance.dict())

    def perform_update(self, instance: Model, schema_instance: NinjaModelSchema) -> Model:
        """Update an existing instance"""
        return schema_instance.update(instance, schema_instance.dict(exclude_unset=True))

    def perform_delete(self, instance: Model) -> None:
        """Delete an instance"""
        instance.delete()
