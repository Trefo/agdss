from webclient.models import *

from django.contrib import admin
from django.db.models import Count



admin.site.register(Image)
admin.site.register(ImageLabel)
admin.site.register(ImageSourceType)
admin.site.register(CategoryType)
admin.site.register(ImageFilter)


class ImageLabelInline(admin.TabularInline):
    model = ImageLabel
    fields = ( 'categoryType', 'parentImage', 'imageWindow', 'pub_date')
    readonly_fields = ('parentImage', 'categoryType', 'imageWindow', 'pub_date')
    extra = 0
    show_change_link = True
    can_delete = False
    ordering = ['pub_date']

class LabelerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        #('Image Labels', {'fields': ['ImageLabel_set']})
    ]
    inlines = [ImageLabelInline]
admin.site.register(Labeler, LabelerAdmin)
