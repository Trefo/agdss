from django.template import loader
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from webclient.models import *
from datetime import datetime
from django.template import RequestContext

import os


from .models import Image

def index(request):
    latest_image_list = os.listdir('/home/jdas/Dropbox/Research/agriculture/agdss/image-store/')
    template = loader.get_template('webclient/index.html')

    context = {
        'latest_image_list': latest_image_list,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def applyLabels(request):
    dict = json.load(request)
    label_list_ = dict['label_list']
    image_name = dict['image_name']
    category_name = dict['category_name']
    parentImage_ = Image.objects.all().filter(name = image_name);
    if not parentImage_:
        sourceType = ImageSourceType(description='machine')
        sourceType.save()
        parentImage_ = Image(name=image_name, path = '/static/image-store/', description = category_name, source = sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        labelObject = ImageLabels(parentImage = parentImage_, labelShapes=label_list_)
        labelObject.save()
    print label_list_
    return JsonResponse(label_list_[0],safe=False)


def loadLabels(request):
    parentImage_ = request.GET['image_name']
    print parentImage_

    image = Image.objects.all().filter(name = parentImage_)
    if not image:
        print 'why here?'
        sourceType = ImageSourceType(description='machine')
        sourceType.save()
        parentImage_ = Image(name=parentImage_, path='/static/image-store/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        label_list = ImageLabels.objects.all().filter(parentImage=image[0])

    responseText = ''
    responseText = responseText + label_list[0].labelShapes
    return JsonResponse(responseText, safe=False)


def purge(request):
    Image.objects.all().delete()
    ImageLabels.objects.all().delete()
    return HttpResponse("PURGED TABLES!")

