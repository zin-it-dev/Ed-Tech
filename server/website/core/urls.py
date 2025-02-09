from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.conf.urls.static import static

from .settings import base

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
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
