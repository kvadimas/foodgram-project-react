from rest_framework import routers
from django.urls import path, include

from api.views import TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
