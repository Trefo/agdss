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
    latest_image_list = os.listdir('/Users/jdas/Dropbox/Research/agriculture/agdss/image-store/')
    template = loader.get_template('webclient/index.html')

    context = {
        'latest_image_list': latest_image_list,
        'selected_image': latest_image_list[0],
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def applyLabels(request):
    dict = json.load(request)
    label_list_ = dict['label_list']
    image_name = dict['image_name']
    category_name = dict['category_name']
    sourceType = ''
    categoryType = ''
    parentImage_ = Image.objects.all().filter(name = image_name);
    categoryTypeList = CategoryType.objects.all().filter(category_name=category_name);
    if (categoryTypeList):
        categoryType = categoryTypeList[0]
    else:
        categoryType = CategoryType(category_name=category_name, pub_date=datetime.now())
        categoryType.save()

    sourceTypeList = ImageSourceType.objects.all().filter(description="human");
    if (sourceTypeList):
        sourceType = sourceTypeList[0]
    else:
        sourceType = ImageSourceType(description="human", pub_date=datetime.now())
        sourceType.save()


    if not parentImage_:

        parentImage_ = Image(name=image_name, path = '/static/image-store/', description = "development test", source = sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        labelObject = ImageLabels(parentImage = parentImage_[0], labelShapes=label_list_,pub_date=datetime.now(),categoryType=categoryType)
        labelObject.save()
    return JsonResponse(label_list_,safe=False)


def loadLabels(request):
    parentImage_ = request.GET['image_name']
    label_list = []
    sourceType = ''
    categoryType = ''
    sourceTypeList = ImageSourceType.objects.all().filter(description="human");
    if (sourceTypeList):
        sourceType = sourceTypeList[0]
    else:
        sourceType = ImageSourceType(description="human", pub_date=datetime.now())
        sourceType.save()


    image = Image.objects.all().filter(name = parentImage_)
    if not image:
        parentImage_ = Image(name=parentImage_, path='/static/image-store/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        label_list = ImageLabels.objects.all().filter(parentImage=image[0]).order_by('pub_date').last()

    responseText = ''
    if(label_list):
        responseText = responseText + label_list.labelShapes
    return JsonResponse(responseText, safe=False)


def purge(request):
    Image.objects.all().delete()
    ImageLabels.objects.all().delete()
    ImageSourceType.objects.all().delete()
    CategoryType.objects.all().delete()
    return HttpResponse("PURGED TABLES!")

