from wand.image import Image as WandImage
import StringIO
from webclient.models import Image, ImageLabel

def convertSVGtoPNG(file):
    #Convert copy of image to new format
    with WandImage(file).clone() as img:
        img.format = 'png'
        img.save(filename='C:/Users/Sandeep/test.png')


def stringToSVGString(str):
    height = 386
    width = 241


    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' \
       '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' \
       '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" ' \
       'xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" xml:space="preserve" height=%i ' \
        ' width=%i>%s</svg>' %(height, width, str)

def convertSVGs(LabelList):
    for label in LabelList:
        convertSVGtoPNG(stringToSVGString(label.labelShapes))
