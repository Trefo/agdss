from __future__ import unicode_literals

from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    imageType = models.ForeignKey(ImageType, on_delete=models.CASCADE)
    sourceType = models.ForeignKey(SourceType, on_delete=models.CASCADE)

class ImageType(models.Model):
    desc = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class SourceType(models.Model):
    desc = models.CharField(max_length=200)
