import pytest

from rest_framework import status
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class TestCategoryList(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("", include("apis.urls")),
    ]

    @pytest.mark.django_db
    def test_can_get_category_list(self):
        url = reverse("category-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 8)
