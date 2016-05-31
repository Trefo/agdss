from __future__ import unicode_literals

from datetime import datetime
from django.db import models


class CategoryType(models.Model):
    category_name = models.CharField(default='unknown', max_length=100, unique=True)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return 'Category name: ' + self.category_name


class ImageSourceType(models.Model):
    description = models.CharField(default='unknown',max_length=200, unique=True)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return 'Description: ' + self.description


class Image(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    source = models.ForeignKey(ImageSourceType, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    #TODO: Cascade if last entry is deleted
    categoryType = models.ManyToManyField(CategoryType)
    class Meta:
        unique_together = ('name', 'path')
    def __unicode__(self):
        return 'Name: ' + self.name


class ImageLabel(models.Model):
    parentImage = models.ForeignKey(Image, on_delete=models.CASCADE)
    categoryType = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    labelShapes = models.TextField(max_length=10000)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return 'Image: ' + self.parentImage.name + ' | Category: ' + self.categoryType.category_name



