from rest_framework import serializers

from recipes.models import Recipe, Tag, RecipeIngredient
from users.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(source="ingredient.measurement_unit")
    id = serializers.ReadOnlyField(source="ingredient.id")

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    tegs = TagSerializer(many=True)
    author = UserSerializer(many=False)
    ingredients = RecipeIngredientSerializer(many=True, source="recipeingredient_set")

    class Meta:
        model = Recipe
        fields = "__all__"
