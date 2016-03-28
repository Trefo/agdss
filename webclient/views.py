from django.template import loader
from django.http import *


from .models import Image

def index(request):
    latest_image_list = Image.objects.order_by('-pub_date')[:5]
    template = loader.get_template('webclient/index.html')
    context = {
        'latest_image_list': latest_image_list,
    }
    return HttpResponse(template.render(context, request))


def applyLabels(request):
    return HttpResponse(request.GET['label_list']);