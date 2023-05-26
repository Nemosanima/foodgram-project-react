from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from recipes.models import Tag
from .serializers import TagSerializer
from .mixins import ListRetrieveMixin
from .serializers import CustomUserSerializer


User = get_user_model()


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
