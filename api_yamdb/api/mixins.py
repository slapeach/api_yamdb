from rest_framework import viewsets, mixins



class ListCreateDestroyMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin, viewsets.GenericViewSet):
    search_fields = ('name',)
    lookup_field = 'slug'
