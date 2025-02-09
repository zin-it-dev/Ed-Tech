from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .common import CommonSerializer, TimeStampSerializer, TaggedObjectSerializer
from .models import Category, Course, Lesson, Chapter


class CategorySerializer(CommonSerializer, TimeStampSerializer):
    class Meta(CommonSerializer.Meta, TimeStampSerializer.Meta):
        model = Category
        fields = CommonSerializer.Meta.fields + ["label"] + TimeStampSerializer.Meta.fields


class CourseSerializer(TaggedObjectSerializer, TimeStampSerializer):

    category = serializers.StringRelatedField()

    class Meta(TaggedObjectSerializer.Meta, TimeStampSerializer.Meta):
        model = Course
        fields = (
            TaggedObjectSerializer.Meta.fields
            + ["title", "image", "description", "category"]
            + TimeStampSerializer.Meta.fields
        )


class ChapterSerializer(
    NestedHyperlinkedModelSerializer, TaggedObjectSerializer, TimeStampSerializer
):
    parent_lookup_kwargs = {
        "course_slug": "course__slug",
    }

    course = serializers.StringRelatedField()

    class Meta(TaggedObjectSerializer.Meta, TimeStampSerializer.Meta):
        model = Chapter
        fields = (
            TaggedObjectSerializer.Meta.fields
            + ["title", "description", "course"]
            + TimeStampSerializer.Meta.fields
        )


class LessonSerializer(
    NestedHyperlinkedModelSerializer, TaggedObjectSerializer, TimeStampSerializer
):
    parent_lookup_kwargs = {
        "lesson_slug": "lesson__slug",
        "course_slug": "course__slug__slug",
    }

    class Meta(TaggedObjectSerializer.Meta, TimeStampSerializer.Meta):
        model = Lesson
        fields = (
            TaggedObjectSerializer.Meta.fields
            + ["title", "content"]
            + TimeStampSerializer.Meta.fields
        )
