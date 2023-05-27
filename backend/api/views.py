from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from recipes.models import Tag
from .serializers import TagSerializer
from .mixins import ListRetrieveMixin
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny


User = get_user_model()


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

