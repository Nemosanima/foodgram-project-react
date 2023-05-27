from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, CustomUserSerializer, IngredientSerializer, GetRecipeSerializer
from .mixins import ListRetrieveMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


User = get_user_model()


class TagViewSet(ListRetrieveMixin):
    """ViewSet для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientViewSet(ListRetrieveMixin):
    """ViewSet для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class CustomUserViewSet(UserViewSet):
    """ViewSet для пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['GER'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        return Response({'data': request.user})


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetRecipeSerializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_user_model(Recipe, id=pk)
        pass





