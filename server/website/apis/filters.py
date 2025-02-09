from django_filters import rest_framework as filters

from .models import Course, Chapter, Lesson


class BaseFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="iexact")
    created_after = filters.DateFilter(field_name="date_created", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="date_created", lookup_expr="lte")

    class Meta:
        fields = ["tags", "created_after", "created_before"]


class BaseSearchOrdering:
    search_fields = ["title"]
    ordering_fields = ["title", "is_active", "date_created"]


class CourseFilter(BaseFilter):
    category = filters.CharFilter(field_name="category__slug", lookup_expr="iexact")

    class Meta(BaseFilter.Meta):
        model = Course
        fields = BaseFilter.Meta.fields + ["category"]


class ChapterFilter(BaseFilter):
    course = filters.CharFilter(field_name="course__slug", lookup_expr="iexact")

    class Meta(BaseFilter.Meta):
        model = Chapter
        fields = BaseFilter.Meta.fields + ["course"]


class LessonFilter(BaseFilter):
    chapter = filters.CharFilter(field_name="chapter__slug", lookup_expr="iexact")

    class Meta(BaseFilter.Meta):
        model = Lesson
        fields = BaseFilter.Meta.fields + ["chapter"]
