from PIL import Image as PILImage
from webclient.models import *
import convert_images
import numpy
#import scipy
import random

def calculate_entropy_map(image, category):
    images = ImageLabel.objects.all().filter(categoryType=category)
    #aggregrate_array = numpy.full((241,386, len(images)), 255, dtype=numpy.uint8)
    aggregrate_array = [[[] for y in range(386)] for x in range(241)]
    for i, label in enumerate(images):
        #npImg = numpy.array(convert_images.getLabelImagePILFile(label), copy=True)

        #if npImg is None or npImg.shape != aggregrate_array[:,:,i].shape:
        #    continue
        #print numpy.array(convert_images.getLabelImagePILFile(label))
        imgList = numpy.asarray(convert_images.getLabelImagePILFile(label)).tolist()
        if not imgList and not imgList[0]:
            return

        imageWindow = label.imageWindow
        if imageWindow.x >= len(imgList) or imageWindow.x + imageWindow.length > len(imgList):
            return  #"x out of bounds"
        if imageWindow.y >= len(imgList[0]) or imageWindow.y + imageWindow.width > len(imgList):
            return  #"y out of bounds"

        for x in range(imageWindow.x, imageWindow.x + imageWindow.length):
            for y in range(imageWindow.y, imageWindow.y + imageWindow.width):
                #print '%d %d' %(x, y)
                aggregrate_array[x][y].append(imgList[x][y])

    print calculateEntropy(aggregrate_array)

def calculateEntropy(arr):
    binArr = [[numpy.bincount(numpy.array(y, dtype=numpy.uint8)) for y in x] for x in arr]
    probArr = [[y.astype(float)/numpy.sum(y) for y in x] for x in binArr]
    return #[[scipy.stats.entropy(y) for y in x] for x in probArr]


def getImageWindow(image):
    return getRandomImageWindow(image)

def getRandomImageWindow(image):
    retDict = {'width':300, 'height': 300}
    retDict['x'] = random.randrange(0, image.width - retDict['width'])
    retDict['y'] = random.randrange(0, image.height - retDict['height'])
    return retDict
