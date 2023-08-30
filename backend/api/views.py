from django.contrib.auth import get_user_model
from django.db import connection, models
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import filters, response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeShortSerializer, RecipeShowSerializer,
                             TagSerializer, UserSerializer, FollowSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, 
                            RecipeIngredient, ShoppingCart, Tag)
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

    def get_queryset(self):
        user = self.request.user
        if self.action == "create":
            queryset = Recipe.objects.prefetch_related(
                "recipeingredient_set__ingredient", "recipetag_set__tag"
            ).all()
        else:
            queryset = self.queryset

        if user.is_authenticated:
            # Аннотация к каждому объекту Recipe, указывающая,
            # находится ли он в избранном текущего пользователя
            favorites_subquery = Favorite.objects.filter(
                user=user,
                recipe=models.F("pk")
            )

            # Аннотация для проверки наличия объекта Recipe
            # в корзине покупок текущего пользователя
            shopping_cart_subquery = ShoppingCart.objects.filter(
                user=user,
                recipe=models.F("pk")
            )

            queryset = queryset.annotate(
                is_favorite=models.Exists(favorites_subquery),
                is_in_shopping_cart=models.Exists(shopping_cart_subquery)
            )
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
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shoppingcart__user=request.user
            )
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
            )

        # Временный файл PDF в памяти
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Добавляем шрифт
        dejavu_file = "fonts/DejaVuSans.ttf"
        dejavu_font = ttfonts.TTFont("DejaVuSans", dejavu_file)
        pdfmetrics.registerFont(dejavu_font)

        # Добавление списка покупок на страницу PDF
        x_offset = 50
        y_offset = letter[1] - 100
        pdf.setFont("DejaVuSans", 12)
        for line in shopping_list.splitlines():
            pdf.drawString(x_offset, y_offset, line)
            y_offset -= 20

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        file = "shopping_list"
        response = FileResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file}.pdf"'
        return response


class IngredientViewSet(ModelViewSet):
    """Вьсет модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CastomUserViewSet(UserViewSet):
    """Вьсет модели USER"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination

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
