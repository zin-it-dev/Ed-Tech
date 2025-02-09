from drf_excel.mixins import XLSXFileMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class SlugLookupMixin(XLSXFileMixin):
    lookup_field = "slug"

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context["header"] = (
            self.request.GET["fields"].split(",") if "fields" in self.request.GET else None
        )
        return context

    @property
    def filename(self):
        model_name = self.queryset.model.__name__.lower()
        return f"{model_name}_export.xlsx"


class FiltersMixin:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
