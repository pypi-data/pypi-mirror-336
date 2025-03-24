from typing import Any, Dict, TypeVar, Union
from django.db.models import Model
from ninja import Schema

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)
ListSchemaType = TypeVar("ListSchemaType", bound=Schema)
DetailSchemaType = TypeVar("DetailSchemaType", bound=Schema)

class ListModelMixin:
    """
    List a queryset.
    """
    def list(self) -> Union[list[Any], Dict[str, Any]]:
        """
        List objects from the queryset. If pagination is enabled,
        returns a paginated response.
        """
        queryset = self.get_queryset()
        if hasattr(self, 'pagination_class') and self.pagination_class:
            return self.paginate_queryset(queryset)
        return list(queryset)

class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, payload: CreateSchemaType) -> ModelType:
        """
        Create a new object instance.
        """
        return self.perform_create(payload)

    def perform_create(self, schema_instance: CreateSchemaType) -> ModelType:
        """
        Perform the creation of a new object instance.
        Override this method to add custom behavior.
        """
        return schema_instance.create(schema_instance.dict())

class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, id: Any) -> ModelType:
        """
        Retrieve a specific object by ID.
        """
        return self.get_object(id)

class UpdateModelMixin:
    """
    Update a model instance.
    """
    def update(self, id: Any, payload: UpdateSchemaType) -> ModelType:
        """
        Update an existing object instance.
        """
        instance = self.get_object(id)
        return self.perform_update(instance, payload)

    def perform_update(self, instance: ModelType, schema_instance: UpdateSchemaType) -> ModelType:
        """
        Perform the update of an object instance.
        Override this method to add custom behavior.
        """
        return schema_instance.update(instance, schema_instance.dict(exclude_unset=True))

class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, id: Any) -> None:
        """
        Delete an object instance.
        """
        instance = self.get_object(id)
        self.perform_destroy(instance)

    def perform_destroy(self, instance: ModelType) -> None:
        """
        Perform the deletion of an object instance.
        Override this method to add custom behavior.
        """
        instance.delete()
