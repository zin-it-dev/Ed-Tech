from rest_framework.pagination import PageNumberPagination


class BaseSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"


class LargeResultsSetPagination(BaseSetPagination):
    # page_size = 20
    # max_page_size = 100
    page_size = 1
    max_page_size = 10


class StandardResultsSetPagination(BaseSetPagination):
    # page_size = 50
    # max_page_size = 200
    page_size = 1
    max_page_size = 10
