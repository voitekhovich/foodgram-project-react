from app.models import UserSubscribe
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework import serializers, status
from djoser.views import UserViewSet

User = get_user_model()


class SetLimitPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 100


class CustomUserViewSet(UserViewSet):
    pagination_class = SetLimitPagination

    @action(detail=False)
    def subscriptions(self, request):
        """Список авторов, на которых подписан пользователь"""
        user = request.user
        authors = User.objects.filter(following__user=user)
        # author__following__user
        print(authors)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=('get', 'delete'))
    def subscribe(self, request, id=None):
        """Подписаться/отписаться на автора."""

        author = get_object_or_404(User, id=id)
        user = request.user

        if request.method == 'DELETE':
            UserSubscribe.objects.filter(author=author, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        if UserSubscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора')

        UserSubscribe.objects.create(author=author, user=user)
        serializer = self.get_serializer(author)
        return Response(serializer.data)
