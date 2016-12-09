from django import forms
from webclient.models import Image
import requests

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name','description','categoryType','source','path','upload' )
