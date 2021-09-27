from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet


class SetLimitPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 100


class CustomUserViewSet(UserViewSet):
    pagination_class = SetLimitPagination
