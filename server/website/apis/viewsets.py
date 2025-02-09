from rest_framework import viewsets, mixins

from .mixins import SlugLookupMixin


class SlugReadOnlyViewSet(SlugLookupMixin, viewsets.ReadOnlyModelViewSet):
    pass


class SlugListViewSet(SlugLookupMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
