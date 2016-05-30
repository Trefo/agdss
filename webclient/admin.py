from django.contrib import admin
from webclient.models import Image, ImageLabel, ImageSourceType, CategoryType

admin.site.register(Image)
admin.site.register(ImageLabel)
admin.site.register(ImageSourceType)
admin.site.register(CategoryType)

