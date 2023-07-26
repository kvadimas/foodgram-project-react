from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField('Уникальный слаг', max_length=200, unique=True)
