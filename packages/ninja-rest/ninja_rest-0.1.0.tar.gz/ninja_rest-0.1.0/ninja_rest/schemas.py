from datetime import datetime
from typing import Any, Dict, Type, Optional, List
from django.db import models
from ninja import Schema

class NinjaModelSchema(Schema):
    """
    A Schema class that provides DRF-like model serializer functionality
    """
    class Config:
        model: Optional[Type[models.Model]] = None
        fields: List[str] = ['__all__']
        exclude: List[str] = []
        read_only_fields: List[str] = []
        extra = 'allow'

    @classmethod
    def from_model(cls, model: Type[models.Model], **kwargs):
        """Create schema from Django model"""
        fields = kwargs.pop('fields', cls.Config.fields)
        exclude = kwargs.pop('exclude', cls.Config.exclude)
        read_only = kwargs.pop('read_only_fields', cls.Config.read_only_fields)

        attrs = {}
        for field in model._meta.fields:
            if fields != '__all__' and field.name not in fields:
                continue
            if field.name in exclude:
                continue
            
            field_type = cls._get_field_type(field)
            if field_type:
                attrs[field.name] = field_type
                if field.name in read_only:
                    attrs[f'_{field.name}_readonly'] = True

        return type(f'{model.__name__}Schema', (cls,), attrs)

    @staticmethod
    def _get_field_type(model_field: models.Field) -> Any:
        """Map Django model field to Pydantic field type"""
        mapping = {
            models.CharField: str,
            models.TextField: str,
            models.IntegerField: int,
            models.BooleanField: bool,
            models.DateTimeField: datetime,
            models.ForeignKey: int,
            models.AutoField: int,
        }
        
        field_class = type(model_field)
        field_type = mapping.get(field_class)
        
        if field_type:
            return Optional[field_type] if model_field.null else field_type
        return Any

    def create(self, validated_data: Dict[str, Any]) -> models.Model:
        """Create a model instance"""
        model = self.Config.model
        if not model:
            raise ValueError("Config.model must be set")
        return model.objects.create(**validated_data)

    def update(self, instance: models.Model, validated_data: Dict[str, Any]) -> models.Model:
        """Update a model instance"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
