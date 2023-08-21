from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from termcolor import colored

from api.serializers import (
    RecipeShowSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeShortSerializer
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart,
    RecipeIngredient
)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def dispatch(self, request, *args, **kwargs):
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
    
    def get_queryset(self):
        print(self.action)
        if self.action =='create':
            return Recipe.objects.prefetch_related(
                'recipeingredient_set__ingredient',
                'recipetag_set__tag'
            ).all()
        return super().get_queryset()

    def get_serializer_class(self):
        print("<>", self.action)
        if self.action in ('list', 'retrieve'):
            return RecipeShowSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == 'POST':
            Favorite.objects.create(
                recipe=recipe,
                user=user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == 'POST':
            ShoppingCart.objects.create(
                recipe=recipe,
                user=user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        print(colored('download_shopping_cart', 'red'))
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        print(colored('add ingredients', 'red'))

        shopping_list = 'Купить в магазине:'
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}"
                ",\n")
        file = 'shopping_list'
        response = HttpResponse(shopping_list, 'Content-Type: application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response

    def dispatch(self, request, *args, **kwargs):
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




