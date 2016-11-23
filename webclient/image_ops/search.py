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
    for idx,patch in enumerate(labelPatch(map(lambda label:list([parentImg(label), labels(label)]),labelList))):
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

def labelFromLabelIndex(labelIndex):
    categories = CategoryType.objects.all().filter(category_name='tomatoes')
    catTomatoes = categories[0]
    return ImageLabel.objects.all()[labelIndex]

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

def plotPatchList(labelList):
    nrows=5 
    ncols=5
    dpi = 40.0
    xpixels, ypixels = 150, 150
    for idx,patch in enumerate(labelSurvey.labelPatch(labelSurvey.reportLabelStats(labelList))):    
        if idx%25==0:
            fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
            plt.subplots(nrows, ncols)
        #fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
        plt.subplot(nrows,ncols,(idx%25)+1)
        plt.imshow(patch)
        
        

    



