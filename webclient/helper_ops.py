from models import *
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from cStringIO import StringIO
from PIL import Image as PILImage
import urllib

def fixAllImagePaths():
    for image in Image.objects.all():
        if image.path[-1] != '/':
            image.path += '/'
            image.save()

#pass request.scheme, request.get_host() from view in same directory as images
def updateAllImageSizes(scheme, host):
    url_check = URLValidator()
    url = str(scheme + '://' + host)
    for image in Image.objects.all():
        try:
            url_check(image.path)
            im_url = image.path + image.name
        except ValidationError, e:
            im_url = url + image.path + '/' + image.name
        image.width, image.height = PILImage.open(StringIO(urllib.urlopen(im_url).read())).size
        image.save()
