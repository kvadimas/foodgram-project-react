from django.contrib.auth import get_user_model
from django.db import connection
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import (CreateUserSerializer,
                             IngredientSerializer, RecipeCreateSerializer,
                             RecipeShortSerializer, RecipeShowSerializer,
                             TagSerializer, UserSerializer, FollowSerializer)
from api.services import get_shopping_list
from recipes.models import (Favorite, Ingredient, Recipe, ShoppingCart, Tag)
from users.models import Follow

User = get_user_model()


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
        "recipeingredient_set__ingredient", "tags"
    ).select_related("author").all().order_by("id")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        if self.action == "create":
            queryset = Recipe.objects.prefetch_related(
                "recipeingredient_set__ingredient", "recipetag_set__tag"
            ).all()
        else:
            queryset = self.queryset
        if user.is_authenticated:
            queryset = Recipe.objects.with_favorite_and_shoppingcart(user)
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeShowSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def user_action(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeShortSerializer(recipe)
        err = {'errors': 'Вы уже совершали это действие!'}
        if request.method == "POST":
            if model.objects.filter(recipe=recipe, user=user).exists():
                return Response(err, status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(recipe=recipe, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            object = model.objects.filter(user=user, recipe=recipe)
            if not object.exists():
                return Response(err, status=status.HTTP_400_BAD_REQUEST)
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        """Добавить, удалить в избранное."""
        return self.user_action(request, pk, Favorite)

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        """Добавить, удалить лист покупок."""
        return self.user_action(request, pk, ShoppingCart)

    @action(detail=False, methods=["GET"])
    def download_shopping_cart(self, request):
        """Скачать лист покупок."""
        user = request.user
        shopping_file = get_shopping_list(user)
        file = "shopping_list"
        response = FileResponse(shopping_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file}.pdf"'
        return response


class IngredientViewSet(ModelViewSet):
    """Вьсет модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class CastomUserViewSet(UserViewSet):
    """Вьсет модели USER"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer = CreateUserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()

    @action(
        detail=True,
        methods=["POST", "delete"],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == "POST":
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == "DELETE":
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
