from django.contrib import admin
from webclient.models import Image, ImageLabels, ImageSourceType

admin.site.register(Image)
admin.site.register(ImageLabels)
admin.site.register(ImageSourceType)
