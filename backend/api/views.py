from rest_framework.viewsets import ModelViewSet

from api.serializers import RecipeSerializer, TagSerializer
from recipes.models import Recipe, Tag


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def dispatch(self, request, *args, **kwargs):
        # print(request)
        res = super().dispatch(request, *args, **kwargs)
        from django.db import connection

        print(len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return res
