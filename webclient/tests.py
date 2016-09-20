import django.test
import unittest
import django.db
from webclient.models import *

#Models test:

class CategoryTypeModelTestCase(django.test.TestCase):

    def test_category_name_unique(self):
        CategoryType(category_name="test").save()
        self.assertRaises(django.db.IntegrityError, lambda: CategoryType(category_name="test").save())