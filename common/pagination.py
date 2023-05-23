from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_query_param = 'offset'
    page_size_query_param = 'limit'
    invalid_page_message = _('Invalid offset.')

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset=queryset, request=request, view=view)
        except NotFound as _:
            return []

    def get_paginated_response(self, data):
        res = {
            'count': self.page.paginator.count,
            'data': data
        }
        return Response(res)
