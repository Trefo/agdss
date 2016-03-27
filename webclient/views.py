from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Image

def index(request):
    latest_image_list = Image.objects.order_by('-pub_date')[:5]
    template = loader.get_template('webclient/index.html')
    context = {
        'latest_image_list': latest_image_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, image_id):
    return HttpResponse("You're looking at image %s." % image_id)

def results(request, image_id):
    response = "You're looking at the results of image %s."
    return HttpResponse(response % image_id)

def label(request, image_id):
    return HttpResponse("You're labeling on image %s." % image_id)