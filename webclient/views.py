from django.template import loader
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from webclient.models import *
from datetime import datetime
from django.template import RequestContext

import os


from .models import Image

def index(request):
    #latest_image_list = os.listdir('C:/Users/Sandeep/Dropbox/kumar-prec-ag/tag_images') # '/Users/jdas/Dropbox/Research/agriculture/agdss/image-store/')
    latest_image_list = Image.objects.all()
    template = loader.get_template('webclient/index.html')

    context = {
        'latest_image_list': latest_image_list,
        'selected_image': latest_image_list[0],
    }
    return HttpResponse(template.render(context, request))


def results(request):
    template = loader.get_template('webclient/results.html')
    context = {}
    return HttpResponse(template.render(context, request))
@csrf_exempt
def applyLabels(request):
    dict = json.load(request)
    label_list_ = dict['label_list']
    image_name = dict['image_name']
    path = dict['path']
    category_name = dict['category_name']
    sourceType = ''
    categoryType = ''
    parentImage_ = Image.objects.all().filter(name=image_name, path=path);
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


#    if not parentImage_:
#        parentImage_ = Image(name=image_name, path = '/static/tag_images/', description = "development test", source = sourceType, pub_date=datetime.now())
#        parentImage_.save()
 #   else:
    labelObject = ImageLabel(parentImage = parentImage_[0], labelShapes=label_list_,pub_date=datetime.now(),categoryType=categoryType)
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
        parentImage_ = Image(name=parentImage_, path='/static/tag_images/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
        parentImage_.save()
    else:
        label_list = ImageLabel.objects.all().filter(parentImage=image[0]).order_by('pub_date').last()

    responseText = ''
    if(label_list):
        responseText = responseText + label_list.labelShapes
    return JsonResponse(responseText, safe=False)



@require_GET
def getInfo(request):
    if not 'image_name' in request.GET or not 'path' in request.GET:
        return HttpResponseBadRequest("Missing 'image_name or 'path'")
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
        return HttpResponseBadRequest("Could not find image with name " + request.GET['image_name'] + " and path " + request.GET['path'])
        #img = Image(name=parentImage_, path='/static/tag_images/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
        #img.save()
    #else:
    label_list = ImageLabel.objects.all().filter(parentImage=image[0]).order_by('pub_date').last()

    response = {}
    if label_list:
        response['labels'] = json.loads(label_list.labelShapes)
    else:
        response['labels'] = ''
    response['path'] = image[0].path
    response['categories'] = [c.category_name for c in image[0].categoryType.all()]
    return JsonResponse(response, safe=False)



@require_GET
def getNextImage(request):
    return

#TODO: Remove csrf_exempt
@csrf_exempt
def purge(request):
    Image.objects.all().delete()
    ImageLabel.objects.all().delete()
    ImageSourceType.objects.all().delete()
    CategoryType.objects.all().delete()
    return HttpResponse("PURGED TABLES!")



#TODO: Check for bad input
'''
Request: POST
{
    path: location of image (not including image name itself. E.g. '/home/self/image-location/'). REQUIRED
    image-name:name of image REQUIRED
    description: A description NOT REQUIRED
    source_description: Description of image_source. NOT REQUIRED
    category: Category of the image (e.g. 'apple'). REQUIRED.
}

'''
@csrf_exempt
@require_POST
def addImage(request):
    #Validate input
    if not ('image-name' in request.POST and  'path' in request.POST and 'category' in request.POST):
        return HttpResponseBadRequest("Missing required input")


    #Get or create ImageSourceType
    desc = request.POST.get('source_description', default="human")
    imageSourceTypeList = ImageSourceType.objects.all().filter(description = desc)
    if imageSourceTypeList:
        sourceType = imageSourceTypeList[0]
    else:
        sourceType = ImageSourceType(description=request.POST.get('source_description', default="human"), pub_date=datetime.now())
        sourceType.save()

    #Get CategoryType entry or add one if necessary.
    cn = request.POST.get('category', 'unknown')
    categoryTypeList = CategoryType.objects.all().filter(category_name = cn)
    if categoryTypeList:
        categoryType = categoryTypeList[0]
    else:
        categoryType = CategoryType(category_name=request.POST.get('category', 'unknown'))
        categoryType.save()

    imageList = Image.objects.all().filter(name=request.POST['image-name'], path=request.POST['path'], description=request.POST.get('description', default=''), source=sourceType)
    if imageList:
        img = imageList[0]
    else:
        img = Image(name=request.POST['image-name'], path=request.POST['path'], description=request.POST.get('description', default=''), source=sourceType)
        img.save()
    img.categoryType.add(categoryType)
    #imgLabel = ImageLabel(parentImage=img, categoryType=categoryType, pub_date=datetime.now())
    #imgLabel.save()
    return HttpResponse("Added image " + request.POST['image-name'])



'''
Request: POST
{
    path: location of image (not including image name itself. E.g. '/home/self/image-location/'). REQUIRED
    image-name:name of image REQUIRED
    description: A description CHANGED IF INCLUDED
    source_description: Description of image_source. CHANGED IF INCLUDED
    add_category: Category of the image (e.g. 'apple') to be added to the list. UPDATED IF INCLUDED
    remove_category: Category of the image (e.g. 'apple') to be added to the list. UPDATED IF INCLUDED
}

'''
@csrf_exempt
@require_POST
def updateImage(request):
    #Validate input
    if not ('image-name' in request.POST and  'path' in request.POST):
        return HttpResponseBadRequest("Missing required input")
    image = Image.objects.all().filter(name = request.POST['image-name'], path=request.POST['path'])[0]
    if 'description' in request.POST:
        image.description = request.POST['description']
    if 'source-description' in request.POST:
        image.description = request.POST['source-description']
    if 'add_category' in request.POST:
        cats = CategoryType.objects.all().filter(category_name=request.POST['add_category'])
        if not cats or not image.filter(categoryType=cats[0]):
            if cats:
                cat = cats[0]
            else:
                cat = CategoryType(category_name=request.POST['add_category'])
                cat.save()
            image.categoryType.add(cat)
    if 'remove_category' in request.POST:
        cats = CategoryType.objects.all().filter(category_name=request.POST['remove_category'])
        if cats and image.filter(categoryType=cats[0]):
            image.categoryType.remove(cat)
    return HttpResponse("Made changes")
