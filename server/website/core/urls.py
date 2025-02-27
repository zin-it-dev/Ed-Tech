from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.conf.urls.static import static
from django.views.i18n import set_language

from .settings import base
from .admin import admin_statistics_view

admin.autodiscover()

urlpatterns = [
    path(
        "admin/statistics/", admin.site.admin_view(admin_statistics_view), name="admin-statistics"
    ),
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("set-language/", set_language, name="set_language"),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("", include("apis.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
    re_path(r"^ckeditor5/", include("django_ckeditor_5.urls")),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if base.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))] + static(
        base.MEDIA_URL, document_root=base.MEDIA_ROOT
    )
