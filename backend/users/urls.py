from rest_framework import routers
from django.urls import path, include

from users.views import CastomUserViewSet

router = routers.DefaultRouter()
router.register('user', CastomUserViewSet)

urlpatterns = [
    path('', include('djoser.urls.authtoken')),
    path('me/', include(router.urls)),
]
