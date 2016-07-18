from PIL import Image as PILImage
from webclient.models import *
import convert_images
import numpy

def calculate_entropy_map(image, category):
    images = ImageLabel.objects.all().filter(categoryType=category)
    aggregrate_array = numpy.full((241,386, len(images)), 255, dtype=numpy.uint8)
    for i, label in enumerate(images):
        npImg = numpy.array(convert_images.getLabelImagePILFile(label), copy=True)
        if npImg is None or npImg.shape != aggregrate_array[:,:,i].shape:
            continue
        imageWindow = label.ImageWindow

        #Set all non-window values to 255
        npImg[0:imageWindow.x, 0:imageWindow.y] = 255
        npImg[-1:imageWindow.x + imageWindow.length:-1, -1:imageWindow.y + imageWindow.width:-1] = 255
        #aggregrate_array = numpy.concatenate((aggregrate_array, npImg), axis=2)
        aggregrate_array[:,:,i] = npImg


    #aggregrate_array = numpy.delete(aggregrate_array, 255, 2)
    aggregrate_array = aggregrate_array[aggregrate_array[:,:] != 255]
    print aggregrate_array
    #countedArray = numpy.apply_along_axis(numpy.bincount, 2, aggregrate_array)
    print countedArray
#Removes 255 if found
def calculateEntropy():
    return