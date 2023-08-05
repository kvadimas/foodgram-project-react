from django.urls import include, path
from rest_framework import routers

from api.views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet
)
from users.views import CastomUserViewSet

router = routers.DefaultRouter()
router.register("user", CastomUserViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet)
router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path('/users/me/', include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
