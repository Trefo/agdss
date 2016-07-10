import json
import os.path
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Count
from django.http import *
from django.http import JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from django.conf import settings
from .models import *

def index(request):
    template = loader.get_template('webclient/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def view_label(request):
    template = loader.get_template('webclient/view_label.html')
    context = {}
    return HttpResponse(template.render(context, request))


def label(request):
    #latest_image_list = os.listdir('C:/Users/Sandeep/Dropbox/kumar-prec-ag/tag_images') # '/Users/jdas/Dropbox/Research/agriculture/agdss/image-store/')
    latest_image_list = Image.objects.all()
    template = loader.get_template('webclient/label.html')
    if latest_image_list:
        context = {
            'latest_image_list': latest_image_list,
            'selected_image': latest_image_list[0],
        }
    else:
        context = {}
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
    image_filters = dict['image_filters']


    sourceType = ''
    categoryType = ''
    parentImage_ = Image.objects.all().filter(name=image_name, path=path)
    categoryTypeList = CategoryType.objects.all().filter(category_name=category_name)
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
    image_filter_obj = ImageFilter(brightness=image_filters['brightness'],
                                   contrast=image_filters['contrast'],
                                   saturation=image_filters['saturation'],
                                   imageLabel=labelObject)
    image_filter_obj.save()

    from convert_images import convertSVG
    convertSVG(labelObject)
    return HttpResponse(label_list_)

@require_GET
def loadLabels(request):
    if 'image_name' not in request.GET or 'path' not in request.GET:
        print(request.GET['path'] + ' ' + request.GET['image_name'])
        return HttpResponseBadRequest('Path and Image Name required')

    parentImage_ = request.GET['image_name']
    label_list = []
    sourceType = ''
    categoryType = ''
    # sourceTypeList = ImageSourceType.objects.all().filter(description="human");
    # if (sourceTypeList):
    #     sourceType = sourceTypeList[0]
    # else:
    #     sourceType = ImageSourceType(description="human", pub_date=datetime.now())
    #     sourceType.save()

    image = Image.objects.all().filter(name=request.GET['image_name'], path=request.GET['path'])
    # if not image:
    #     parentImage_ = Image(name=parentImage_, path='/static/tag_images/',description='test generation at serverside', source=sourceType, pub_date=datetime.now())
    #     parentImage_.save()
    if not image:
        return HttpResponseBadRequest("No such image found")
    label_list = ImageLabel.objects.all().filter(parentImage=image[0]).order_by('pub_date').last()

    responseText = ''
    if(label_list):
        responseText = responseText + label_list.labelShapes
    return JsonResponse(responseText, safe=False)



@require_GET
def getInfo(request):
    if 'image_name' not in request.GET or 'path' not in request.GET:
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
        response['label'] = label_list.labelShapes
    else:
        response['label'] = ''
    response['path'] = image[0].path
    response['categories'] = [c.category_name for c in image[0].categoryType.all()]
    return JsonResponse(response, safe=False)


@require_GET
def getNewImage(request):
    if not 'image_name' in request.GET or not 'path' in request.GET:
        hasPrior = False
    else:
        hasPrior = True
        #return HttpResponseBadRequest("Missing image name or path")

    if len(Image.objects.all()) == 0:
        return HttpResponseBadRequest("No images in database")


    ##Choose image


    #Random choice
    # if len(Image.objects.all()) > 1 and hasPrior:
    #     img = choice(Image.objects.all().exclude(name=request.GET['image_name'], path=request.GET['path']))
    # else:
    #     img = choice(Image.objects.all())
    #

    #Least number of labels which was not just seen
    img = Image.objects.all()
    if hasPrior and len(Image.objects.all()) > 1:
        img = img.exclude(name=request.GET['image_name'], path=request.GET['path'])
    img = img.annotate(count=Count('imagelabel')).order_by('count')[0]



    label_list = ImageLabel.objects.all().filter(parentImage=img).order_by('pub_date').last()
    response = {
        'path': img.path,
        'image_name': img.name,
        'categories': [c.category_name for c in img.categoryType.all()]
            }
    if label_list:
        response['labels'   ] = label_list.labelShapes
    else:
        response['labels'] = ''

    return JsonResponse(response)


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
    image_name:name of image REQUIRED
    description: A description NOT REQUIRED
    source_description: Description of image_source. NOT REQUIRED
    category: Category of the image (e.g. 'apple'). REQUIRED.
}

'''
@csrf_exempt
@require_POST
def addImage(request):
    #Validate input
    if not ('image_name' in request.POST and  'path' in request.POST and 'category' in request.POST):
        return HttpResponseBadRequest("Missing required input")
    if request.POST['category'] == '':
        return HttpResponseBadRequest("Missing category")

    #Determine wheter 'path' is URL or file path
    url_check = URLValidator()
    try:
        url_check(request.POST['path'])
    except ValidationError, e:
        #Convert Filepath to webpath if necessary
        ##Check if path is in STATIC_ROOT (https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory)
        root = os.path.join(os.path.realpath(settings.STATIC_ROOT), '')
        path_dir = os.path.realpath(request.POST['path'])

        if not os.path.commonprefix([root, path_dir]) == root:
            return HttpResponseBadRequest(
                "Image in unreachable location. Make sure that it is in a subdirectory of " + settings.STATIC_ROOT +".\n")
        path = os.path.relpath(path_dir, root)
        path = '/webclient' + settings.STATIC_URL + path

    if path[-1] != '/':
        path += '/'

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

    imageList = Image.objects.all().filter(name=request.POST['image_name'], path=path, description=request.POST.get('description', default=''), source=sourceType)
    if imageList:
        img = imageList[0]
    else:
        img = Image(name=request.POST['image_name'], path=path, description=request.POST.get('description', default=''), source=sourceType)
        img.save()
    img.categoryType.add(categoryType)
    #imgLabel = ImageLabel(parentImage=img, categoryType=categoryType, pub_date=datetime.now())
    #imgLabel.save()
    return HttpResponse("Added image " + request.POST['image_name'] + '\n')



'''
Request: POST
{
    path: location of image (not including image name itself. E.g. '/home/self/image-location/'). REQUIRED
    image_name:name of image REQUIRED
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
    if not ('image_name' in request.POST and  'path' in request.POST):
        return HttpResponseBadRequest("Missing required input")
    image = Image.objects.all().filter(name = request.POST['image_name'], path=request.POST['path'])[0]
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


@csrf_exempt
@require_POST
def convertAll(request):
    from convert_images import convertAll
    convertAll(request.POST.get('reconvert', False))
    return HttpResponse('Ok')


@csrf_exempt
@require_GET
def unlabeledImages(request):
    images = Image.objects.all().filter(imagelabel__isnull=True).distinct()
    return HttpResponse("Images: " + ','.join(map(str, images)) )

@csrf_exempt
@require_GET
def numImageLabels(request):
    images = Image.objects.all().annotate(num=Count('imagelabel')).order_by('-num')
    print(images)
    return HttpResponse("Images: " + ','.join(map(str, images)) )
@csrf_exempt
@require_POST
def combineAllImages(request):
    thresholdPercent = int(request.POST.get('thresholdPercent', 50))
    from convert_images import combineImageLabels
    combineImageLabels(Image.objects.all()[0], thresholdPercent)
    return HttpResponse("OK")