# Ninja REST

A Django REST Framework-inspired package built on top of Django Ninja, providing familiar DRF-like features with the modern benefits of Django Ninja.

## Features

- Serializer-like Schema classes with field validation
- ViewSet-like API controllers
- Authentication mixins
- Permission classes
- Pagination support
- Filtering and ordering
- Nested relationship handling

## Installation

```bash
pip install ninja_rest
```

## Quick Start Guide

### 1. Basic Setup

First, add 'ninja_rest' to your INSTALLED_APPS:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'ninja_rest',
]
```

### 2. Define Your Models

```python
# models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
```

### 3. Create Schemas

```python
# schemas.py
from ninja_rest import NinjaModelSchema
from django.contrib.auth.models import User
from .models import Post

class UserSchema(NinjaModelSchema):
    class Config:
        model = User
        fields = ['id', 'username', 'email']

class PostSchema(NinjaModelSchema):
    author: UserSchema

    class Config:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author']
```

### 4. Create ViewSets

```python
# views.py
from ninja_rest import NinjaViewSet
from ninja_rest.permissions import IsAuthenticated
from ninja_rest.pagination import PageNumberPagination
from .schemas import PostSchema
from .models import Post

class PostViewSet(NinjaViewSet):
    schema = PostSchema
    queryset = Post.objects.select_related('author')
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Custom queryset filtering
        if self.request.query_params.get('my_posts'):
            return self.queryset.filter(author=self.request.user)
        return self.queryset
```

### 5. Register URLs

```python
# urls.py
from ninja import Router
from .views import PostViewSet

api = Router()

# This will create the following endpoints:
# GET /posts/ - List all posts
# POST /posts/ - Create a new post
# GET /posts/{id}/ - Retrieve a post
# PUT /posts/{id}/ - Update a post
# DELETE /posts/{id}/ - Delete a post
PostViewSet.register(api, 'posts')
```

## Advanced Usage

### Custom Authentication

```python
from ninja_rest.authentication import TokenAuthentication

class CustomTokenAuth(TokenAuthentication):
    def authenticate(self, request, token):
        try:
            return CustomToken.objects.get(key=token).user
        except CustomToken.DoesNotExist:
            return None

class SecureViewSet(NinjaViewSet):
    authentication_classes = [CustomTokenAuth]
```

### Custom Permissions

```python
from ninja_rest.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, obj):
        return obj.author == request.user

class PostViewSet(NinjaViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

### Custom Pagination

```python
from ninja_rest.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    class Input(Schema):
        page: int = 1
        page_size: int = 50

class PostViewSet(NinjaViewSet):
    pagination_class = CustomPagination
```

### Schema Validation

```python
from ninja import Schema
from ninja_rest import NinjaModelSchema

class PostCreateSchema(NinjaModelSchema):
    title: str
    content: str

    class Config:
        model = Post
        fields = ['title', 'content']

    @validator('title')
    def title_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError('Title must be capitalized')
        return v
```

## Testing

```python
from django.test import TestCase
from ninja.testing import TestClient

class TestPostViewSet(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user('testuser')

    def test_create_post(self):
        response = self.client.post(
            '/api/posts/',
            json={
                'title': 'Test Post',
                'content': 'Test Content'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 201)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
