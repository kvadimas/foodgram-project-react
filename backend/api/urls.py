from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from rest_framework import routers
from users.views import CastomUserViewSet

router = routers.DefaultRouter()
router.register("users", CastomUserViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet)
router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
