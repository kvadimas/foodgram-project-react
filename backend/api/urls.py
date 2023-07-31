from django.urls import include, path
from rest_framework import routers

from api.views import RecipeViewSet, TagViewSet
from users.views import CastomUserViewSet

router = routers.DefaultRouter()
router.register('user', CastomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    #path('/users/me/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
