from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductsPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
