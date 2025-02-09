from django.test import TestCase

from apis.models import Category


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.get_or_create(label="DevOps", slug="devops")

    def test_label(self):
        category = Category.objects.get(label='DevOps')
        self.assertEqual(category.label, "DevOps")
