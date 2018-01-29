from __future__ import unicode_literals

from datetime import datetime
from unicodedata import decimal

from django.db import models



class Color(models.Model):
    red = models.PositiveSmallIntegerField(default=0)
    green = models.PositiveSmallIntegerField(default=0)
    blue = models.PositiveSmallIntegerField(default=0)
    class Meta:
        unique_together = ('red', 'green', 'blue')

    def __str__(self):
        return "rgb({}, {}, {})".format(self.red, self.green, self.blue)

def get_default_Color():
    default_Color = Color.objects.all()
    if default_Color:
        default_Color = default_Color[0]
    else:
        default_Color = Color()
        default_Color.save()
    return default_Color.id

class CategoryType(models.Model):
    category_name = models.CharField(default='unknown', max_length=100, unique=True)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, default=get_default_Color)

    def __str__(self):
        return 'Category name: ' + self.category_name



class ImageSourceType(models.Model):
    description = models.CharField(default='unknown',max_length=200, unique=True)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
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
    def __str__(self):
        return 'Name: ' + self.name


from django.contrib.auth.models import User
class Labeler(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
class ImageWindow(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('x', 'y', 'width', 'height')

    def __str__(self):
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

    def __str__(self):
        return 'Image: ' + self.parentImage.name + ' | Category: ' + self.categoryType.category_name  + ' | Labeler: ' + str(self.labeler)





class ImageFilter(models.Model):
    brightness = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    contrast = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    saturation = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    imageLabel = models.ForeignKey(ImageLabel, on_delete=models.CASCADE, null=True, blank=True, default=None)
    labeler = models.ForeignKey(Labeler, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return 'ImageFilter: brightness:' + str(self.brightness) + ' contrast: ' + str(self.contrast)\
               + ' saturation: ' + str(self.saturation) + ' labeler: ' + str(self.labeler)

