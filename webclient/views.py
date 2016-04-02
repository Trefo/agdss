from django.forms import forms
from django.template import loader
from django.http import *
from webclient.models import *
from datetime import datetime
import os

from .models import Image

def index(request):
    latest_image_list = os.listdir('/home/jdas/Dropbox/Research/agriculture/agdss/image-store/')
    template = loader.get_template('webclient/index.html')

    context = {
        'latest_image_list': latest_image_list,
    }
    print template.render(context, request)
    return HttpResponse(template.render(context, request))


def applyLabels(request):
    label_list_ = request.GET['label_list']
    sourceType = ImageSourceType(description='machine')
    sourceType.save()
    parentImage_ = Image(name=request.GET['image_name'], path = '/static/image-store/', description = 'test generation at serverside', source = sourceType, pub_date=datetime.now())
    parentImage_.save()
    for labelJSON in label_list_:
        print labelJSON
        labelObject = ImageLabels(parentImage = parentImage_, labelShapes=labelJSON)
        labelObject.save()
    return HttpResponse(label_list_)


def loadLabels(request):
    label_list_ = request.GET['image_name']
    sourceType = ImageSourceType(description='machine')
    sourceType.save()
    parentImage_ = Image(name=request.GET['image_name'], path = '/static/image-store/', description = 'test generation at serverside', source = sourceType, pub_date=datetime.now())
    parentImage_.save()
    for labelJSON in label_list_:
        print labelJSON
        labelObject = ImageLabels(parentImage = parentImage_, labelShapes=labelJSON)
        labelObject.save()
    return HttpResponse(label_list_)

