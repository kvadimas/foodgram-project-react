from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeCreateSerializer
)
from recipes.models import Recipe, Tag, Ingredient


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def dispatch(self, request, *args, **kwargs):
        # print(request)
        res = super().dispatch(request, *args, **kwargs)
        from django.db import connection

        print(len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return res


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.prefetch_related(
        'recipeingredient_set__ingredient',
        'tags',
        'author'
    ).all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ('create',):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        # print(request)
        res = super().dispatch(request, *args, **kwargs)
        from django.db import connection

        print(len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return res


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def dispatch(self, request, *args, **kwargs):
        # print(request)
        res = super().dispatch(request, *args, **kwargs)
        from django.db import connection

        print(len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return res
