from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import User, Category, Course, Lesson, Tag


class CommonAdmin:
    pass


class LessonAdmin(admin.ModelAdmin):
    widgets = {
        "content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="lesson")
    }


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag)
