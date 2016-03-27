from __future__ import unicode_literals

from datetime import datetime
from django.db import models

class ImageType(models.Model):
    description = models.CharField(max_length=200)

class ImageSourceType(models.Model):
    description = models.CharField(max_length=200)

class Image(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    type = models.ForeignKey(ImageType, on_delete=models.CASCADE)
    source = models.ForeignKey(ImageSourceType, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)


