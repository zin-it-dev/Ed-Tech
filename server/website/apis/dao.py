from .models import Category, Course, Lesson, Chapter


def load_common(model, order_by="-date_created", **kwargs):
    queryset = model.objects.filter(is_active=True, **kwargs)

    if order_by:
        queryset = queryset.order_by(order_by)

    return queryset.all()


def load_categories():
    return load_common(Category)


def load_courses():
    return load_common(Course).select_related("category").prefetch_related("tags")


def load_chapters(course=None):
    return (
        Chapter.objects.filter(is_active=True, course__slug=course)
        .select_related("course")
        .prefetch_related("tags")
        .all()
    )


def load_lessons(course=None, chapter=None):
    return (
        Lesson.objects.filter(is_active=True, chapter__course__slug=course, chapter__slug=chapter)
        .select_related("chapter")
        .prefetch_related("tags")
        .all()
    )
