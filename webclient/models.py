from __future__ import unicode_literals

from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    context = models.CharField(max_length=500)
    objectClass = models.ForeignKey(ImageType, on_delete=models.CASCADE)

    created_date = models.DateTimeField('date created')
    imageType = models.ForeignKey(ImageType, on_delete=models.CASCADE)

class ImageType(models.Model):
    desc = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class ObjectClass(models.Model):
    desc = models.CharField(max_length=200)
