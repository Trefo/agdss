import PIL
from webclient.models import *
import convert_images
import numpy

def calculate_entropy_map(image, category):
    for label in ImageLabel.objects.all().filter(categoryType=category):
        npImg = numpy.array(convert_images.getLabelImagePILFile(label), copy=True)
        imageWindow = label.ImageWindow

        #Set all non-window values to 255
        npImg[0:imageWindow.x, 0:imageWindow.y] = 255
        npImg[-1:imageWindow.x + imageWindow.length:-1, -1:imageWindow.y + imageWindow.width:-1] = 255
