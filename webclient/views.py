from django.shortcuts import render_to_response
from django.template import loader
from django.http import *
from django.views.decorators.csrf import csrf_exempt


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
    print request.POST['label_list']
    # label_list_ = dict['label_list']
    # image_name = dict['image_name']
    parentImage_ = Image.objects.all().filter(name = image_name);
    if not parentImage_:
        sourceType = ImageSourceType(description='machine')
        sourceType.save()
        parentImage_ = Image(name=request.GET['image_name'], path = '/static/image-store/', description = 'test generation at serverside', source = sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        for labelJSON in label_list_:
            labelObject = ImageLabels(parentImage = parentImage_[0], labelShapes=labelJSON)
            print labelJSON
            labelObject.save()
    csrfContext = RequestContext(request)
    return render_to_response(label_list_, csrfContext)


def loadLabels(request):
    parentImage_ = request.GET['image_name']
    image = Image.objects.all().filter(name = parentImage_)
    if not image:
        sourceType = ImageSourceType(description='machine')
        sourceType.save()
        parentImage_ = Image(name=parentImage_, path='/static/image-store/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        label_list = ImageLabels.objects.all().filter(parentImage=image[0])
    if not label_list:
        label_list_ = ''
    else:
        label_list_ = label_list[0].labelShapes
    return HttpResponse(label_list_)


def purge(request):
    Image.objects.all().delete()
    ImageLabels.objects.all().delete()
    return HttpResponse("PURGED TABLES!")

