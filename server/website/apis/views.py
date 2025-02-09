from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters import rest_framework as filters

from .serializers import CategorySerializer, CourseSerializer, ChapterSerializer, LessonSerializer
from .dao import load_categories, load_courses, load_lessons, load_chapters
from .viewsets import SlugReadOnlyViewSet, SlugListViewSet
from .paginators import LargeResultsSetPagination, StandardResultsSetPagination
from .mixins import FiltersMixin
from .filters import CourseFilter, BaseSearchOrdering, LessonFilter, ChapterFilter


class CategoryViewSet(SlugListViewSet):
    """
    A read-only viewset for managing categories. 📚
    """

    queryset = load_categories()
    serializer_class = CategorySerializer


class CourseViewSet(SlugReadOnlyViewSet, FiltersMixin, BaseSearchOrdering):
    """
    A read-only viewset for managing courses. 🎓
    """

    queryset = load_courses()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    pagination_class = StandardResultsSetPagination


class ChapterViewSet(SlugReadOnlyViewSet, FiltersMixin, BaseSearchOrdering):
    """
    A read-only viewset for managing chapters. 📖
    """

    serializer_class = ChapterSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = ChapterFilter

    def get_queryset(self):
        return load_chapters(course=self.kwargs.get("course_slug"))


class LessonViewSet(SlugReadOnlyViewSet, FiltersMixin, BaseSearchOrdering):
    """
    A read-only viewset for managing lessons. 🔖
    """

    serializer_class = LessonSerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = LessonFilter

    def get_queryset(self):
        return load_lessons(
            course=self.kwargs.get("course_slug"), chapter=self.kwargs.get("chapter_slug")
        )
