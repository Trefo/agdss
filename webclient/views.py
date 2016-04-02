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
    return HttpResponse(template.render(context, request))


def applyLabels(request):
    label_list_ = request.GET['label_list']
    #sourceType = ImageSourceType(description='machine')
    #sourceType.save()
    #parentImage_ = Image(name=request.GET['image_name'], path = '/static/image-store/', description = 'test generation at serverside', source = sourceType, pub_date=datetime.now())
    #parentImage_.save()
    image_name = request.GET['image_name']
    parentImage_ = Image.objects.all().filter(name = image_name);
    for labelJSON in label_list_:
        labelObject = ImageLabels(parentImage = parentImage_[0], labelShapes=labelJSON)
        labelObject.save()
    return HttpResponse(label_list_)


def loadLabels(request):
    parentImage_ = request.GET['image_name']
    image = Image.objects.all().filter(name = parentImage_)
    label_list = ImageLabels.objects.all().filter(parentImage=image[0])
    return HttpResponse(label_list[0].labelShapes)

