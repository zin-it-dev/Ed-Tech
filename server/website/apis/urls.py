from django.urls import path, include
from rest_framework_nested import routers

from .views import CategoryViewSet, CourseViewSet, LessonViewSet, get_stats_courses

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"courses", CourseViewSet, basename="course")

courses_router = routers.NestedSimpleRouter(router, r"courses", lookup="course")
courses_router.register(r"lessons", LessonViewSet, basename="lessons")

urlpatterns = [
    path("", include(router.urls)),
    path(r"", include(courses_router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # Analysis & Statistics
    path("chart/courses/", get_stats_courses, name="chart-courses"),
]
