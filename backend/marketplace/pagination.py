from rest_framework.pagination import CursorPagination as BaseCursorPagination

class CursorPagination(BaseCursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'
