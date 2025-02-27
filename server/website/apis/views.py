from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters import rest_framework as filters
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .serializers import CategorySerializer, CourseSerializer, LessonSerializer
from .dao import (
    CategoryRepository,
    CourseRepository,
    LessonRepository,
    AnalyticsRepository,
)
from .viewsets import SlugReadOnlyViewSet, SlugListViewSet
from .paginators import LargeResultsSetPagination, StandardResultsSetPagination
from .mixins import FiltersMixin
from .filters import CourseFilter, BaseSearchOrdering, LessonFilter


# Analysis & Statistics


@staff_member_required
def get_stats_courses(request):
    amount = [data["amount"] for data in AnalyticsRepository.stats_courses_by_category()]
    labels = [data["title"] for data in AnalyticsRepository.stats_courses_by_category()]

    return JsonResponse(
        {
            "data": {"labels": labels, "datasets": [{"data": amount, "label": "Amount"}]},
        }
    )


# APIs


class CategoryViewSet(SlugListViewSet):
    """
    A read-only viewset for managing categories. 📚
    """

    queryset = CategoryRepository().get_all()
    serializer_class = CategorySerializer


class CourseViewSet(SlugReadOnlyViewSet, FiltersMixin, BaseSearchOrdering):
    """
    A read-only viewset for managing courses. 🎓
    """

    queryset = CourseRepository().get_all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    pagination_class = StandardResultsSetPagination


class LessonViewSet(SlugReadOnlyViewSet, FiltersMixin, BaseSearchOrdering):
    """
    A read-only viewset for managing lessons. 🔖
    """

    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = LessonFilter

    def get_queryset(self):
        return LessonRepository().get_all(obj_slug=self.kwargs.get("course_slug"))
