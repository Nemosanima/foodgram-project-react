from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient, Recipe
from .serializers import (TagSerializer, CustomUserSerializer,
                          IngredientSerializer, GetRecipeSerializer,
                          ShortRecipeSerializer, PostRecipeSerializer, SubscriptionSerializer)
from .mixins import ListRetrieveMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, ShoppingCart, RecipeIngredient
from django.db.models import Sum
from django.http import HttpResponse
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CustomFilterForRecipes


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

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], serializer_class=None)
    def subscriptions(self, request):
        user = request.user
        favorites = user.followers.all()
        users_id = [favorite_instance.author.id for favorite_instance in favorites]
        users = User.objects.filter(id__in=users_id)
        paginated_queryset = self.paginate_queryset(users)
        serializer = SubscriptionSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilterForRecipes

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetRecipeSerializer
        return PostRecipeSerializer

    @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепт уже есть в избранном.')
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(instance=recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=user, recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепта нет в ибранном.')
            Favorite.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепт уже есть в списке покупок.')
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(instance=recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепта нет в списке покупок.')
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recipes_id = [item.recipe.id for item in shopping_cart]
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes_id
        ).values('ingredient').annotate(amount=Sum('amount'))
        final_list = 'Список покупок от Foodgram\n\n'
        for item in ingredients:
            ingredient = Ingredient.objects.get(id=item.get('ingredient'))
            amount = item.get('amount')
            final_list += (
                f'{ingredient.name} ({ingredient.measurement_unit}) {amount}\n'
            )

        filename = 'foodgram_shopping_list.txt'
        response = HttpResponse(final_list[:-1], content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response


