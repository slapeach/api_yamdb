from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin)


class ListCreateDestroyMixin(ListModelMixin, CreateModelMixin,
                             DestroyModelMixin, GenericViewSet):
    search_fields = ('name',)
    lookup_field = 'slug'
