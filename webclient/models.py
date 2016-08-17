from __future__ import unicode_literals

from datetime import datetime
from unicodedata import decimal

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
    width = models.PositiveSmallIntegerField(default=1920)
    height = models.PositiveSmallIntegerField(default=1080)
    #TODO: Cascade if last entry is deleted
    categoryType = models.ManyToManyField(CategoryType)
    class Meta:
        unique_together = ('name', 'path')
    def __unicode__(self):
        return 'Name: ' + self.name


from django.contrib.auth.models import User
class Labeler(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return str(self.user)
class ImageWindow(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('x', 'y', 'width', 'height')

    def __unicode__(self):
        return '(x,y)=(%d,%d), width: %d, height: %d' %(self.x,self.y,self.width, self.height)

def getDefaultImageWindowId():
    defaultImageWindowList = ImageWindow.objects.all().filter(x=0, y=0, width=1920, height=1080)
    if defaultImageWindowList:
        defaultImageWindow = defaultImageWindowList[0]
    else:
        defaultImageWindow = ImageWindow(x=0, y=0, width=1920, height=1080)
        defaultImageWindow.save()
    return defaultImageWindow.id

class ImageLabel(models.Model):
    parentImage = models.ForeignKey(Image, on_delete=models.CASCADE)
    categoryType = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    labelShapes = models.TextField(max_length=10000)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    labeler = models.ForeignKey(Labeler, on_delete=models.CASCADE, null=True, blank=True, default=None)
    imageWindow = models.ForeignKey(ImageWindow, on_delete=models.CASCADE, default=getDefaultImageWindowId)
    timeTaken = models.PositiveIntegerField(null=True, default=None)
    #ip_address = models.GenericIPAddressField(default=None, blank=True, null=True)

    def __unicode__(self):
        return 'Image: ' + self.parentImage.name + ' | Category: ' + self.categoryType.category_name  + ' | Labeler: ' + str(self.labeler)





class ImageFilter(models.Model):
    brightness = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    contrast = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    saturation = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    imageLabel = models.ForeignKey(ImageLabel, on_delete=models.CASCADE, null=True, blank=True, default=None)
    labeler = models.ForeignKey(Labeler, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __unicode__(self):
        return 'ImageFilter: brightness:' + str(self.brightness) + ' contrast: ' + str(self.contrast)\
               + ' saturation: ' + str(self.saturation) + ' labeler: ' + str(self.labeler)



