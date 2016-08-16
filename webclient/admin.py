from django.contrib import admin

from webclient.models import *

admin.site.register(Image)
admin.site.register(ImageLabel)
admin.site.register(ImageSourceType)
admin.site.register(CategoryType)
admin.site.register(ImageFilter)

