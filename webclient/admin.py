from webclient.models import *

from django.contrib import admin
from django import forms
from django.utils.html import format_html




admin.site.register(Image)
#admin.site.register(ImageLabel)
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

@admin.register(Labeler)
class LabelerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Label Stats', {'fields': ['number_labeled']})
        #('Image Labels', {'fields': ['ImageLabel_set']})
    ]
    readonly_fields = ('number_labeled', )
    inlines = [ImageLabelInline]

    def number_labeled(self, obj):
        return len(ImageLabel.objects.all().filter(labeler=obj))


class ImageLabelAdminForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = ImageLabel
        widgets = {
            'overlayed_image': forms.ImageField()
        }

@admin.register(ImageLabel)
class ImageLabelAdmin(admin.ModelAdmin):
    list_display = ('parentImage', 'categoryType', 'imageWindow', 'labeler', 'timeTaken', 'pub_date')
    readonly_fields = ('overlayed_image', )

    def overlayed_image(self, obj):
        return format_html('<img src="{}" alt="Rendered Image Label"></>' , '/webclient/get_overlayed_image/%d' % obj.id)
        # blob = RenderSVGString(SVGString(obj.labelShapes))
        # b64 = base64.b64encode(blob)
        # return format_html('<img src="data:image/png;base64,{}" alt="Rendered Image Label"></>',
        #                    b64)
