from django.urls import path, include
from rest_framework_nested import routers

from .views import CategoryViewSet, CourseViewSet, LessonViewSet, ChapterViewSet

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"courses", CourseViewSet, basename="course")

courses_router = routers.NestedSimpleRouter(router, r"courses", lookup="course")
courses_router.register(r"chapters", ChapterViewSet, basename="chapters")

chapters_router = routers.NestedSimpleRouter(courses_router, r"chapters", lookup="chapter")
chapters_router.register(r"lessons", LessonViewSet, basename="lessons")

urlpatterns = [
    path("", include(router.urls)),
    path(r"", include(courses_router.urls)),
    path(r"", include(chapters_router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
