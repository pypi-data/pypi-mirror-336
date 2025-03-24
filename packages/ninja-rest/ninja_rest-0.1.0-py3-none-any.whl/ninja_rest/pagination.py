from typing import Any, List, Optional
from django.db.models import QuerySet
from ninja.pagination import PaginationBase
from ninja import Schema

class PageNumberPagination(PaginationBase):
    """
    DRF-style page number pagination
    """
    class Input(Schema):
        page: int = 1
        page_size: int = 100

    class Output(Schema):
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None
        results: List[Any]

    def paginate_queryset(
        self,
        queryset: QuerySet,
        request,
        page: int = 1,
        page_size: int = 100,
        **params
    ) -> Any:
        # Calculate pagination values
        count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        # Get current page URL
        url = request.build_absolute_uri()
        base_url = url.split('?')[0]
        
        # Calculate next and previous URLs
        next_page = None
        previous_page = None
        
        if end < count:
            next_page = f"{base_url}?page={page + 1}&page_size={page_size}"
        if page > 1:
            previous_page = f"{base_url}?page={page - 1}&page_size={page_size}"

        return self.Output(
            count=count,
            next=next_page,
            previous=previous_page,
            results=list(queryset[start:end])
        )
