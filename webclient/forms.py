from django import forms
from webclient.models import *
import requests
import urllib2

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name','description','categoryType','source','path','upload' )

class CSVForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name','categoryType','source','path' )
