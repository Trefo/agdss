from django.template import loader
from django.http import *
from webclient.models import *
from datetime import datetime


from .models import Image

def index(request):
    latest_image_list = Image.objects.order_by('-pub_date')[:5]
    template = loader.get_template('webclient/index.html')
    context = {
        'latest_image_list': latest_image_list,
    }
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


