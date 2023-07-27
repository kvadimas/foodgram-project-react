from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField('Уникальный слаг', max_length=200, unique=True)


class Recipe(models.Model):
    tegs = models.ManyToManyField(Tag, )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=200)
    image = models.CharField(
        'Ссылка на картинку на сайте',
        max_length=200,
        blank=True,
        null=True
    )
    text = models.CharField('Описание', max_length=200)
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (в минутах)'
    )
