from rest_framework.viewsets import ModelViewSet

from api.serializers import RecipeSerializer, TagSerializer
from recipes.models import Recipe, Tag


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
