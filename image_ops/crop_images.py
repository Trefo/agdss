from PIL import Image as PILImage
from webclient.models import *
import convert_images
import numpy

def calculate_entropy_map(image, category):
    images = ImageLabel.objects.all().filter(categoryType=category)
    #aggregrate_array = numpy.full((241,386, len(images)), 255, dtype=numpy.uint8)
    aggregrate_array = [[[] for y in range(386)] for x in range(241)]
    for i, label in enumerate(images):
        #npImg = numpy.array(convert_images.getLabelImagePILFile(label), copy=True)

        #if npImg is None or npImg.shape != aggregrate_array[:,:,i].shape:
        #    continue

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
        print aggregrate_array



        #Set all non-window values to 255
        #npImg[0:imageWindow.x, 0:imageWindow.y] = 255
        #npImg[0:imageWindow.x] = numpy.delete(npImg[0:imageWindow.x], range(imageWindow.y),1)
        #npImg[-1:imageWindow.x+imageWindow.length:-1] = \
         #   numpy.delete(npImg[-1:imageWindow.x + imageWindow.length:-1],
          #               numpy.s_[-1:imageWindow.y + imageWindow.width:-1],1)

        #npImg[-1:imageWindow.x + imageWindow.length:-1, -1:imageWindow.y + imageWindow.width:-1] = 255
        #aggregrate_array = numpy.concatenate((aggregrate_array, npImg), axis=2)
        #aggregrate_array[:,:,i] = npImg


    #aggregrate_array = numpy.delete(aggregrate_array, 255, 2)
    #print numpy.where(aggregrate_array[:,:,:] == 255)
    #print aggregrate_array[aggregrate_array == 255]
    #print aggregrate_array
    #countedArray = numpy.apply_along_axis(numpy.bincount, 2, aggregrate_array)
    #print countedArray
#Removes 255 if found
def calculateEntropy():
    return