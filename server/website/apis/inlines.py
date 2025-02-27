from django.contrib import admin

from .models import Course, Lesson, Resource


class TagCourseInline(admin.TabularInline):
    model = Course.tags.through


class TagLessonInline(admin.TabularInline):
    model = Lesson.tags.through


class ResourceInline(admin.StackedInline):
    model = Resource
