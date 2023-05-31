from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow

from .filters import CustomFilterForIngredients, CustomFilterForRecipes
from .mixins import ListRetrieveMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, GetRecipeSerializer,
                          IngredientSerializer, PostRecipeSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()


class TagViewSet(ListRetrieveMixin):
    """ViewSet для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(ListRetrieveMixin):
    """ViewSet для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filterset_class = CustomFilterForIngredients


class CustomUserViewSet(UserViewSet):
    """ViewSet для пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        user = request.user
        favorites = user.followers.all()
        users_id = [favorite_instance.author.id for favorite_instance in favorites]
        users = User.objects.filter(id__in=users_id)
        paginated_queryset = self.paginate_queryset(users)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)

        follow_search = Follow.objects.filter(user=user, author=author)

        if request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError('Подписываться на себя запрещено.')
            if follow_search.exists():
                raise exceptions.ValidationError('Вы уже подписаны на этого пользователя.')
            Follow.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not follow_search.exists():
                raise exceptions.ValidationError('Вы не подписаны на этого пользователя.')
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteShoppingCartMixin:
    """Вынес общее для favorite и shopping_cart
    http методы post и delete.
    """

    @staticmethod
    def create(model, recipe_pk, request, error_message):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise exceptions.ValidationError(error_message)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(instance=recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(model, recipe_pk, request, error_message):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if not model.objects.filter(user=user, recipe=recipe).exists():
            raise exceptions.ValidationError(error_message)
        model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilterForRecipes

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetRecipeSerializer
        return PostRecipeSerializer

    @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Рецепт уже есть в избранном.'
            return FavoriteShoppingCartMixin.create(Favorite, pk, request, error_message)
        elif request.method == 'DELETE':
            error_message = 'Рецепта нет в избранном.'
            return FavoriteShoppingCartMixin.delete(Favorite, pk, request, error_message)

    @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Рецепт уже есть в списке покупок.'
            return FavoriteShoppingCartMixin.create(ShoppingCart, pk, request, error_message)
        elif request.method == 'DELETE':
            error_message = 'Рецепта нет в списке покупок.'
            return FavoriteShoppingCartMixin.delete(ShoppingCart, pk, request, error_message)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recipes_id = [item.recipe.id for item in shopping_cart]
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes_id).values('ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        final_list = 'Список покупок от Foodgram\n\n'

        for item in ingredients:
            ingredient_name = item['ingredient__name']
            measurement_unit = item['ingredient__measurement_unit']
            amount = item['amount']
            final_list += f'{ingredient_name} ({measurement_unit}) {amount}\n'

        filename = 'foodgram_shopping_list.txt'
        response = HttpResponse(final_list[:-1], content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

    # @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    # def favorite(self, request, pk=None):
    #     user = self.request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     if request.method == 'POST':
    #         if Favorite.objects.filter(user=user, recipe=recipe).exists():
    #             raise exceptions.ValidationError('Рецепт уже есть в избранном.')
    #         Favorite.objects.create(user=user, recipe=recipe)
    #         serializer = ShortRecipeSerializer(instance=recipe, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     if request.method == 'DELETE':
    #         if not Favorite.objects.filter(user=user, recipe=recipe).exists():
    #             raise exceptions.ValidationError('Рецепта нет в ибранном.')
    #         Favorite.objects.filter(user=user, recipe=recipe).delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(detail=True, methods=('POST', 'DELETE'), permission_classes=[IsAuthenticated])
    # def shopping_cart(self, request, pk=None):
    #     user = self.request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     if request.method == 'POST':
    #         if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
    #             raise exceptions.ValidationError('Рецепт уже есть в списке покупок.')
    #         ShoppingCart.objects.create(user=user, recipe=recipe)
    #         serializer = ShortRecipeSerializer(instance=recipe, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     if request.method == 'DELETE':
    #         if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
    #             raise exceptions.ValidationError('Рецепта нет в списке покупок.')
    #         ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
