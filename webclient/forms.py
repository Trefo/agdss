from django import forms
from webclient.models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('description','categoryType', 'upload', )
