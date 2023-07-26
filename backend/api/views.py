from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from recipes.models import Tag
from api.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
