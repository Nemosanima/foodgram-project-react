from rest_framework import mixins, viewsets


class ListRetrieveMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass
