from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Recipe,
    Tag,
    RecipeIngredient,
    Ingredient,
    Favorite,
    ShoppingCart
)
from users.serializers import UserSerializer
from rest_framework.exceptions import ValidationError


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )
    id = serializers.ReadOnlyField(source="ingredient.id")

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RecipeShowSerializer(serializers.ModelSerializer):
    """ Сериализатор показа модели рецепта. """
    tags = TagSerializer(many=True)
    author = UserSerializer(many=False)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source="recipeingredient_set"
    )
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class IngredientsRecipeCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор записи рецепта. """
    author = UserSerializer(read_only=True)
    ingredients = IngredientsRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'tags',
            'image',
            'cooking_time',
            'ingredients',
            'author'
        )

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({
                'tags': 'Нужно выбрать хотя бы один тег!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Теги должны быть уникальными!'
                })
            tags_list.append(tag)
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients = [
            RecipeIngredient(ingredient=Ingredient.objects.get(id=data['id']),
                             recipe=recipe,
                             amount=data['amount'])
            for data in ingredients
        ]
        RecipeIngredient.objects.prefetch_related('ingredients').bulk_create(
            recipe_ingredients)
        return recipe
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        recipe_ingredients = [
            RecipeIngredient(
                ingredient_id=data['id'],
                recipe=instance,
                amount=data['amount']
            )
            for data in ingredients
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShowSerializer(instance,
                                    context=context).data


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
