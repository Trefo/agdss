from wand.image import Image as WandImage
from wand.color import Color as WandColor
import StringIO
from webclient.models import Image, ImageLabel
from django.conf import settings
import re
import wand.exceptions
import os
from PIL import Image as PILImage
import numpy
import SVGRegex



def convertSVGtoPNG(img_file, foldername, filename, reconvert=False):
    #Convert copy of image to new format
    #print(img_file.getvalue())
    if not img_file:
        #TODO: Some error checking
        return
    #TODO: error checking on foldername and filename
    foldername_ = foldername
    if foldername_[0] == '/' or foldername_[0] == '\\':
        foldername_ = foldername_[1:]
    if foldername_[-1] == '/' or foldername_[-1] == '\\':
        foldername_ = foldername_[:-1]

    if not reconvert and os.path.exists(settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/' + filename + '.png'):
         return settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/' + filename + '.png'
    try:
        #svgs = separatePaths(img_file)
        with WandImage(file=img_file) as img:
            #img.depth = 1
            #img.colorspace = 'gray'

            #print(filename)
	    #print(WandColor('white'))

            img.background_color = WandColor('white')
            img.alpha_channel = 'remove'

            #Convert to black and white
            img.negate()
            img.threshold(0)
            #img.negate()

            img.format = 'png'


            if not os.path.exists(settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/'):
                os.makedirs(settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/')
            img.save(filename=(settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/' + filename + '.png'))
            print("converted Image " + filename)
            return settings.STATIC_ROOT +  settings.LABEL_FOLDER_NAME + foldername + '/' + filename + '.png'
 

    except wand.exceptions.CoderError as e:
        print('Failed to convert: ' + filename + ': '+ str(e))
    except wand.exceptions.MissingDelegateError as e:
        print('DE Failed to convert: ' + filename + ': '+ str(e))
    except wand.exceptions.WandError as e:
	print('Failed to convert ' + filename + ': '+ str(e))

def SVGStringToImageBlob(svg):
    if not svg:
        return
    svgFile = StringIO.StringIO(svg)
    try:
        with WandImage(file=svgFile) as img:
            img.background_color = WandColor('white')
            img.alpha_channel = 'remove'
            # Convert to black and white
            img.negate()
            img.threshold(0)
            img.format = 'png'
            return img.make_blob()
    except wand.exceptions.CoderError as e:
        print('Failed to convert: ' + svg + ': ' + str(e))
    except wand.exceptions.MissingDelegateError as e:
        print('DE Failed to convert: ' + svg + ': ' + str(e))
    except wand.exceptions.WandError as e:
        print('Failed to convert ' + svg + ': ' + str(e))
#Returns array of SVGs each with 1 path
def separatePaths(svg):
    #rePath = r'(<path[^/>]*/>)'
    paths = re.findall(SVGRegex.rePath, svg)
    image, height, width = SVGDimensions(svg)
    images = []
    for path in paths:
        images.append(SVGStringToImageBlob(SVGString(path, height, width)))
    return images

def countableLabel(svgString):
    convertedImages = separatePaths(svgString)
    height, width = SVGDimensions(svgString)[1:]
    image = numpy.zeros((int(height), int(width)), numpy.uint8)
    for convertedImage in convertedImages:
        img = PILImage.open(StringIO.StringIO(convertedImage)).convert("L")
        imgArr = numpy.array(img, copy=True)
        PILImage.fromarray(imgArr, mode='L').show()
        image += imgArr
        #img.show()
    #for i in image * 100:
     #   print i
    #PILImage.fromarray(image * 100, mode='L').show()
    return image
def SVGDimensions(str):
    result = re.search(SVGRegex.reWH, str)
    if result == None:
        return (None, None, None)

    #reFill = r'<path[^/>]*fill\s*=\s*"(?P<fill>[^"]*)"'
    #reStroke = r'<path[^/>]*stroke\s*=\s*"(?P<stroke>[^"]*)"'
    pathFill = '#000001'
    pathStroke = '#000001'

    image = result.group(0)
    height = result.group('height').encode('utf-8')
    width = result.group('width').encode('utf-8')
    return (image, height, width)


#If height and width are defined, image tag is not removed
#Otherwise, height and width are extracted from it and it is removed
def SVGString(DBStr, height=None, width=None):
    addedStr = DBStr
    if height == None or width == None:
        image, height, width = SVGDimensions(DBStr)
        if image:
            addedStr = DBStr.replace(image, '')
    addedStr = addedStr.encode('utf-8')
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' \
             '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"' \
            ' xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" xml:space="preserve" height="%s"' \
             ' width="%s">%s</svg>\n' %(height, width, addedStr)

def labelToSVGStringFile(str):
    SVGStringFile = StringIO.StringIO(SVGString(str))
    SVGStringFile.seek(0)
    return SVGStringFile

def convertSVGs(LabelList, reconvert=False):
    return [convertSVG(label, reconvert) for label in LabelList if label is not None]

def convertSVG(label, reconvert=False):
    return convertSVGtoPNG(img_file=labelToSVGStringFile(label.labelShapes), foldername=label.categoryType.category_name,
                    filename=labelFilename(label),
                    reconvert=reconvert)

def labelFilename(label):
    return 'P%iL%iC%sI%s' % (
            label.parentImage.id, label.id, label.categoryType.category_name, label.parentImage.name)
def convertAll(reconvert=False):
    convertSVGs(ImageLabel.objects.all(), reconvert=reconvert)


def combineImageLabels(image, thresholdPercent=50):
    threshold = thresholdPercent/100.0 * 255
    print(threshold)
    labels = ImageLabel.objects.all().filter(parentImage=image)
    for label in labels:
        countableLabel(label.labelShapes)
        return
        for i in separatePaths(label.labelShapes):
            print(i)
    if not labels:
        return
    return
    #Based on https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil
    filepaths = convertSVGs(labels)
    if not filepaths:
        return
    width, height = PILImage.open(filepaths[0]).size
    N = len(filepaths)
    print(filepaths)
    arr = numpy.zeros((height,width),numpy.float)
    for im in filepaths:
        img = PILImage.open(im).convert('L')
        img.load()
        imarr = numpy.array(img, copy=True, dtype=numpy.float)
        #img.show()
        arr = arr + imarr / N
    arr = numpy.array(numpy.round(arr), dtype=numpy.uint8)
    #for i in arr:
     #   print(i)
    arr[arr <= threshold] = 0  # Black
    arr[arr > threshold] = 255  # White
    out = PILImage.fromarray(arr, mode="L")
    out.save("C:/Users/Sandeep/Dropbox/kumar-prec-ag/temp/%sAverage.png" %image.name)
    out.show()


