from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField("Название", max_length=200)
    color = models.CharField("Цвет в HEX", max_length=7, unique=True)
    slug = models.SlugField("Уникальный слаг", max_length=200, unique=True)

    def __str__(self):
        return f"{self.name}"


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
    )
    tags = models.ManyToManyField(
        Tag,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=200)
    image = models.CharField(
        "Ссылка на картинку на сайте", max_length=200, blank=True, null=True
    )
    text = models.CharField("Описание", max_length=200)
    cooking_time = models.PositiveIntegerField(
        "Время приготовления (в минутах)"
    )


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.measurement_unit}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
