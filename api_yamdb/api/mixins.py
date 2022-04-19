from rest_framework import viewsets, mixins


class ListCreateDestroyMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Миксин на создание, удаление и получение списка"""
    search_fields = ('name',)
    lookup_field = 'slug'
