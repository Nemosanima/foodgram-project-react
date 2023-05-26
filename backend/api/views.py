from rest_framework import mixins, viewsets
from recipes.models import Tag
from .serializers import TagSerializer


class ListRetrieveMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

