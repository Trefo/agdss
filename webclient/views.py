from django.shortcuts import render
from django.http import HttpResponse
from .models import Image

def index(request):
    latest_image_list = Image.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_image_list}
    return render(request, 'webclient/index.html', context)

def detail(request, image_id):
    return HttpResponse("You're looking at image %s." % image_id)

def results(request, image_id):
    response = "You're looking at the results of image %s."
    return HttpResponse(response % image_id)

def label(request, image_id):
    return HttpResponse("You're labeling on image %s." % image_id)