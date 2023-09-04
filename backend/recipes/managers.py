from django.db import models
from django.db.models import Exists, OuterRef


class RecipeManager(models.Manager):
    def with_favorite_and_shoppingcart(self, user):
        from recipes.models import Favorite, ShoppingCart
        favorites_subquery = Favorite.objects.filter(
            user=user,
            recipe=OuterRef("pk")
        )

        shopping_cart_subquery = ShoppingCart.objects.filter(
            user=user,
            recipe=OuterRef("pk")
        )

        queryset = self.get_queryset().annotate(
            is_favorite=Exists(favorites_subquery),
            is_in_shopping_cart=Exists(shopping_cart_subquery)
        )

        return queryset
