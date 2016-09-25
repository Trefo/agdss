import django.test
import unittest
import django.db
from webclient.models import *
import numpy
from PIL import Image as PILImage

#Models test:

class CategoryTypeModelTestCase(django.test.TestCase):

    def test_category_name_unique(self):
        CategoryType(category_name="test").save()
        self.assertRaises(django.db.IntegrityError, lambda: CategoryType(category_name="test").save())

class ImageModelTestCase(django.test.TestCase):
    def test_name_path_unique(self):
        sourceType = ImageSourceType(description='test')
        sourceType.save()
        cat = CategoryType(category_name="test")
        cat.save()
        img = Image(name='test', path='test_path', source=sourceType)
        img.save()
        img.categoryType.add(cat)
        self.assertRaises(django.db.IntegrityError, lambda: Image(name="test", path='test_path', source=sourceType).save())

class ImageWindowModelTestCase(django.test.TestCase):
    pass

class ImageLabelModelTestCase(django.test.TestCase):
    pass


class ImageFilterModelTestCase(django.test.TestCase):
    pass




class GetCroppedImageTestCase(django.test.TestCase):
    def setUp(self):
        height, width = 1000, 1000
        image_arr = numpy.zeros((height, width))
        image_arr[0:height/4][0:width/4] = 125
        pil_image = PILImage.fromarray(image_arr)
        print pil_image.size
        pil_image.show()

    def test_get_geometric_image_window(self):
        pass