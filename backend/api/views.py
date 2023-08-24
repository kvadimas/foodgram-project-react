from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeShortSerializer,
    RecipeShowSerializer,
    TagSerializer,
)
from django.db import connection, models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TagViewSet(ModelViewSet):
    """Вьсет модели Tag"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def dispatch(self, request, *args, **kwargs):
        print("Tag", len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return super().dispatch(request, *args, **kwargs)


class RecipeViewSet(ModelViewSet):
    """Вьсет модели Recipe"""

    queryset = Recipe.objects.prefetch_related(
        "recipeingredient_set__ingredient", "tags", "author"
    ).all()

    def get_queryset(self):
        print(self.action)
        if self.action == "create":
            return Recipe.objects.prefetch_related(
                "recipeingredient_set__ingredient", "recipetag_set__tag"
            ).all()
        return super().get_queryset()

    def get_serializer_class(self):
        print("<>", self.action)
        if self.action in ("list", "retrieve"):
            return RecipeShowSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        """Добавить, удалить в избранное."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == "POST":
            Favorite.objects.create(recipe=recipe, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        """Добавить, удалить лист покупок."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == "POST":
            ShoppingCart.objects.create(recipe=recipe, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            favorite = ShoppingCart.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=False, methods=["GET"])
    def download_shopping_cart(self, request):
        """Скачать лист покупок."""
        ingredients = (
            RecipeIngredient.objects.filter(recipe__shoppingcart__user=request.user)
            .order_by("ingredient__name")
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=models.Sum("amount"))
        )
        shopping_list = "Купить в магазине:"
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}"
                ",\n"
            )
        file = "shopping_list"
        response = HttpResponse(shopping_list, "Content-Type: application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file}.pdf"'
        return response

    def dispatch(self, request, *args, **kwargs):
        print("Recipe", len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return super().dispatch(request, *args, **kwargs)


class IngredientViewSet(ModelViewSet):
    """Вьсет модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def dispatch(self, request, *args, **kwargs):
        print("Ingredient", len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return super().dispatch(request, *args, **kwargs)
