from webclient.models import Image, ImageLabel, CategoryType
from django.conf import settings
from webclient.image_ops import convert_images
from PIL import Image as PILImage
from StringIO import StringIO
import numpy as np
import matplotlib.pyplot as plt
import requests
import urllib2
from webclient.image_ops import convert_images

def reflect(labelList = [ImageLabel.objects.all().last()]):
    allLabels = labelPatch(map(lambda label:[parentImg(label), labels(label)],labelList))
    for idx,patch in enumerate(allLabels):
        if idx%25==0:
            plt.subplots(5, 5)
        plt.subplot(5,5,(idx%25)+1)
        plt.imshow(patch)
    return allLabels

def labels(label):
    npArray = []
    separatedPaths = convert_images.separatePaths(label.labelShapes)
    if len(separatedPaths) > 0:
        imgLabel = plt.imread(StringIO(separatedPaths[0]))
        npArray = np.array(svgStringToXML(label))
    return npArray

def parentImg(label):
    image = label.parentImage
    hostpath = 'http://airborne.ddns.net:8000'
    imageURL = hostpath + image.path + image.name
    return plt.imread(urllib2.urlopen(imageURL), format='jpeg')
    
def labelPatch(labelInfoList):
    allLabelPatches = []
    for labelInfo in labelInfoList:
        vecAll = labelInfo[1]
        imgParent = labelInfo[0]
        if len(vecAll)>0:
            xc=vecAll[:,0].astype(np.float)+vecAll[:,3].astype(np.float)
            yc=vecAll[:,1].astype(np.float)+vecAll[:,4].astype(np.float)
            delta = 1.3*vecAll[:,2].astype(np.float)
            xr=(xc+delta).astype(np.int16)
            yr=(yc+delta).astype(np.int16)
            xl = (xc-delta).astype(np.int16)
            yl = (yc-delta).astype(np.int16)
            for i in range(0,len(vecAll)):
                allLabelPatches.append(imgParent[yl[i]:yr[i],xl[i]:xr[i],:])
    return allLabelPatches


def plotImageWithLabels(vecAll, imgParent):
    dpi = 80.0
    xpixels, ypixels = 1280, 1920
    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)

    plt.imshow(imgParent)
    plt.hold('on')
    plt.scatter(vecAll[:,0].astype(np.float)+vecAll[:,3].astype(np.float), vecAll[:,1].astype(np.float)+vecAll[:,4].astype(np.float), s=vecAll[:,2].astype(np.float)*vecAll[:,2].astype(np.float), facecolors='none', edgecolors='y', marker='o')
    
    
def svgStringToXML(labelDBObj):
    import xml.etree.ElementTree as ET
    svgXML = ET.fromstring(labelDBObj.labelShapes.encode())
    vecAll = []

    for circle in svgXML.findall('{http://www.w3.org/2000/svg}circle'):
        keys = {'cx','cy', 'r'}
        vec = []
        for key in keys:
            vec.append(circle.get(key))
        trans = circle.get('transform')
        exec('xt, yt = ' + trans)
        vec.append(xt)
        vec.append(yt)
        vecAll.append(vec)
    return vecAll
             
def translate(xt,yt):
    return [xt, yt]
             

def plotAllPatchesForLabel(label):
    dpi = 4.0
    xpixels, ypixels = 400, 400
    for idx,img in enumerate(labelSurvey.labelPatch(labelSurvey.reportLabelStats(label))):
        fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
        plt.subplot(25,1,idx+1)
        plt.imshow(val)
        
def trainingsPatchForLabel(label):
    imageParent = parentImg(label)
    imageWindow = label.imageWindow
    x = imageWindow.x
    y = imageWindow.y
    width = imageWindow.width
    height = imageWindow.height 
    croppedImage = imageParent[y-20:(y+height+20),x-20:(x+width+20),:]
    labelImage = convert_images.countableLabel(label.labelShapes)
    croppedLabelImage = labelImage[y-20:(y+height+20),x-20:(x+width+20)]
    return croppedImage,croppedLabelImage



