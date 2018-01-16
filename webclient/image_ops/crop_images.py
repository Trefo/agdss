import numpy

from . import convert_images
from webclient.models import *

#import scipy
import random


NUM_WINDOW_ROWS = 1
NUM_WINDOW_COLS = 1
WINDOW_PADDING = 20
NUM_LABELS_PER_WINDOW = 3

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

    print(calculateEntropy(aggregrate_array))

def calculateEntropy(arr):
    binArr = [[numpy.bincount(numpy.array(y, dtype=numpy.uint8)) for y in x] for x in arr]
    probArr = [[y.astype(float)/numpy.sum(y) for y in x] for x in binArr]
    return #[[scipy.stats.entropy(y) for y in x] for x in probArr]


def getImageWindow(image, user, ignore_max_count=False):
    return getPaddedWindow(image, user, ignore_max_count=ignore_max_count)

def getRandomImageWindow(image):
    retDict = {'width':300, 'height': 300}
    retDict['x'] = random.randrange(0, image.width - retDict['width'])
    retDict['y'] = random.randrange(0, image.height - retDict['height'])
    return retDict


def getGeometricImageWindow(image):
    windowDict = {'width': image.width/4, 'height': image.height/4}
    topLeftArr = []
    for x in range(0, image.width, image.width / 8):
        for y in range(0, image.height, image.height / 8):
            topLeftArr.append((x,y))
    numLabels = len(ImageLabel.objects.all().filter(parentImage=image))
    topLeft = topLeftArr[numLabels % len(topLeftArr)]
    windowDict['x'], windowDict['y'] = topLeft
    return windowDict


def getPaddedWindow(image, user, ignore_max_count=False):

    #Crop out sidemost pixels
    windowWidth = int((image.width - (2* WINDOW_PADDING))/NUM_WINDOW_COLS)
    windowHeight = int((image.height - (2* WINDOW_PADDING))/NUM_WINDOW_ROWS)
    windowDict = {'width': windowWidth, 'height': windowHeight,
                  'padding': WINDOW_PADDING}

    for x in range(WINDOW_PADDING, image.width - WINDOW_PADDING,  windowWidth):
        for y in range(WINDOW_PADDING, image.height - WINDOW_PADDING, windowHeight):
            labels = image.imagelabel_set.all().filter(imageWindow__x=x, imageWindow__y=y)
            print(labels)
            if (ignore_max_count and all(not label.labeler.user.groups.filter(name='god').exists() for label in labels)) or (len(labels) < NUM_LABELS_PER_WINDOW and all(label.labeler.user != user for label in labels)):
                windowDict['x'], windowDict['y'] = (x,y)
                print(windowDict)
                return windowDict
    return None
