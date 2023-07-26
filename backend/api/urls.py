from django.urls import include, path
from rest_framework import routers

from api.views import TagViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
