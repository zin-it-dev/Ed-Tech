from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from .models import Category, Course, Lesson, Tag


class BaseRepository:
    def __init__(self, model: models.Model):
        self.model = model

    def get_all(self):
        return self.model.objects.filter(is_active=True).order_by("-date_created").all()


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Category)


class CourseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Course)

    def get_all(self):
        queryset = super().get_all()
        return queryset.select_related("category").prefetch_related("tags")


class LessonRepository(BaseRepository):
    def __init__(self):
        super().__init__(Lesson)

    def get_all(self, obj_slug):
        try:
            queryset = super().get_all()
            return (
                queryset.filter(course__slug=obj_slug)
                .select_related("course")
                .prefetch_related("tags")
                .all()
            )
        except ObjectDoesNotExist:
            return None


class AnalyticsRepository:
    @staticmethod
    def stats_courses_by_category():
        return (
            Category.objects.annotate(amount=Count("courses"))
            .values("id", "title", "amount")
            .order_by("-amount")
            .all()
        )

    @staticmethod
    def stats_courses_by_tag():
        return (
            Tag.objects.annotate(amount=Count("courses"))
            .values("id", "name", "amount")
            .order_by("-amount")
        )
