from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import User, Category, Course, Lesson, Tag
from .forms import UserChangeForm, UserCreationForm
from .inlines import TagCourseInline, TagLessonInline, ResourceInline
from .actions import export_as_csv, export_as_json, make_actived


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = "-Unknown-"
    list_display = ["is_active", "date_created", "date_updated"]
    ordering = ["date_created", "id"]
    search_fields = ["title"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    date_hierarchy = "date_created"
    list_per_page = 10


class CommonAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["slug"]


class ExcludeTagAdmin(CommonAdmin):
    exclude = ["tags"]


class CategoryAdmin(CommonAdmin):
    list_display = ["title"] + CommonAdmin.list_display


class CourseAdmin(ExcludeTagAdmin):
    inlines = [TagCourseInline]
    list_display = ["title", "banner", "category"] + ExcludeTagAdmin.list_display
    list_select_related = ["category"]
    list_filter = ["category"] + ExcludeTagAdmin.list_filter
    readonly_fields = ["banner"]


class TagAdmin(CommonAdmin):
    list_display = ["title"] + CommonAdmin.list_display


class LessonAdmin(ExcludeTagAdmin):
    widgets = {
        "content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="lesson")
    }
    inlines = [TagLessonInline, ResourceInline]
    list_display = ["title", "content", "course"] + ExcludeTagAdmin.list_display
    list_select_related = ["course"]
    list_filter = ["course"] + ExcludeTagAdmin.list_filter


class UserAdmin(BaseUserAdmin, BaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["username", "avatar_preview", "is_active", "last_login"]
    date_hierarchy = "date_joined"
    list_editable = ["is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    list_filter = ["is_superuser", "is_active", "is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "avatar",
                    "is_active",
                    "date_joined",
                    "last_login",
                ]
            },
        ),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "user_permissions"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password",
                    "confirm_password",
                    "avatar",
                    "username",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ],
            },
        ),
    ]
    ordering = ["email", "first_name", "last_name"]
    filter_horizontal = ["user_permissions"]
    readonly_fields = ["avatar_preview"]


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.add_action(export_as_json, "export_as_json")
admin.site.add_action(export_as_csv, "export_as_csv")
admin.site.add_action(make_actived, "mark_actived")
