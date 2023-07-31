from djoser.views import UserViewSet
from rest_framework import filters, permissions, status
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer
class CastomUserViewSet(UserViewSet):
    """Вьсет модели USER"""
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ['GET', 'POST', 'PATCH', 'DELETE']
