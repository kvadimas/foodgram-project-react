from rest_framework.viewsets import ModelViewSet

from api.serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
