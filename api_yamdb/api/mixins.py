from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin)


class ListCreateDestroyMixin(ListModelMixin, CreateModelMixin,
                             DestroyModelMixin, GenericViewSet):
    """Миксин на создание, удаление и получение списка"""
    search_fields = ('name',)
    lookup_field = 'slug'
