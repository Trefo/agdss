from wand.image import Image as WandImage
import StringIO
from webclient.models import Image, ImageLabel
from django.conf import settings
import re
import wand.exceptions


def convertSVGtoPNG(file, filename):
    #Convert copy of image to new format
    if not file:
        #TODO: Some error checking
        return
    print '%r' %file.read()
    file.seek(0)
    try:
        with WandImage(file=file) as img:
            img.format = 'png'
            img.save(filename=(settings.STATIC_ROOT +  'temp/' + filename + '.png'))
            #img.save(filename=('C:/Users/Sandeep/Dropbox/kumar-prec-ag/test.png'))
            print("converted Image")
    except wand.exceptions.CoderError as e:
        print('Failed to convert: ' + str(e))
    except wand.exceptions.MissingDelegateError as e:
        print('DE Failed to convert: ' + str(e))

def labelToSVGString(str):
    #Find width and height
    reWH = r'<image [^>]*(height="(?P<height>\d+)"[^>]* | width="(?P<width>\d+)"[^>]*){2}[^>]*/>'
    result = re.search(reWH, str)
    if result == None:
        #TODO: Some errory stuff
        return
    height = result.group('height')
    width = result.group('width')
    if height == None or width == None:
        #TODO: Do some error stuff
        return
    print(str)

    SVGStringFile = StringIO.StringIO('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' +
             '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"' +
            ' xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" xml:space="preserve" height="' + height + '"' +
             ' width="' + width + '">' + str.replace(result.group(0), '') +  '</svg>') #%(height, width, str.replace(result.group(0), '')) )
    SVGStringFile.seek(0)

    return SVGStringFile

def convertSVGs(LabelList):
    #convertSVGtoPNG(labelToSVGString(LabelList[3].labelShapes), 'name')
    #return
    for i, label in enumerate(LabelList):
        convertSVGtoPNG(labelToSVGString(label.labelShapes), 'name' + str(i))


def convertAll():
    convertSVGs(ImageLabel.objects.all())
