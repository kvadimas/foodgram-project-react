from api.pagination import CustomPagination
from api.serializers import CustomUserSerializer, FollowSerializer
from django.contrib.auth import get_user_model
from django.db import connection
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import Follow

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    """Вьсет модели USER"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination

    @action(
        detail=True, methods=["POST", "delete"], permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == "POST":
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    def dispatch(self, request, *args, **kwargs):
        print("User", len(connection.queries))
        for q in connection.queries:
            print(">>>>", q["sql"])
        return super().dispatch(request, *args, **kwargs)
