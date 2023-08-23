from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, response
from rest_framework.decorators import action

from api.pagination import CustomPagination
from users.models import Follow
from api.serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    """Вьсет модели USER"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    # filter_fields = ("username",)
    # search_fields = ("username",)
    # lookup_field = "username"
    pagination_class = CustomPagination
    #http_method_names = ["GET", "POST", "DELETE"]

    @action(
        detail=True,
        methods=['POST', 'delete']
        #permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow,
                                             user=user,
                                             author=author)
            subscription.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET',]
        #permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        print(1)
        queryset = User.objects.filter(following__user=user)
        print(2)
        pages = self.paginate_queryset(queryset)
        print(3)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
