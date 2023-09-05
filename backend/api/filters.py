from django_filters import rest_framework as filters
from django_filters import FilterSet, ModelMultipleChoiceFilter

from recipes.models import Ingredient, Tag, Recipe


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug",
    )
    is_favorited = filters.BooleanFilter(
        method="is_favorited_filter"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="is_in_shopping_cart_filter"
    )

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(favorite__user=user)
        else:
            return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(shoppingcart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = [
            "tags",
            "author",
            "is_favorited",
            "is_in_shopping_cart"
        ]
