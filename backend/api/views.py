from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, CustomUserSerializer, IngredientSerializer, GetRecipeSerializer
from .mixins import ListRetrieveMixin
from rest_framework.permissions import AllowAny
from rest_framework import viewsets



User = get_user_model()


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetRecipeSerializer

