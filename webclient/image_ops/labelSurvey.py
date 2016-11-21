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

def reportLabelStats(labelIndex):
    categories = CategoryType.objects.all().filter(category_name='tomatoes')
    catTomatoes = categories[0]
    image = ImageLabel.objects.all()[labelIndex].parentImage
    label = ImageLabel.objects.all()[labelIndex]
    hostpath = 'http://airborne.ddns.net:8000'
    imageURL = hostpath + image.path + image.name
    imgParent = plt.imread(urllib2.urlopen(imageURL), format='jpeg')
    separatedPaths = convert_images.separatePaths(label.labelShapes)
    imgLabel = plt.imread(StringIO(separatedPaths[0]))
    vecAll = np.array(svgStringToXML(label))
    dpi = 80.0
    xpixels, ypixels = 1280, 1920
    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
    plt.imshow(imgParent)
    plt.hold('on')
    plt.scatter(vecAll[:,0].astype(np.float)+vecAll[:,3].astype(np.float), vecAll[:,1].astype(np.float)+vecAll[:,4].astype(np.float), s=vecAll[:,2].astype(np.float)*vecAll[:,2].astype(np.float), facecolors='none', edgecolors='y', marker='o')
    return [image, label, imgParent, imgLabel, vecAll,plt]
    
    
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
             
        
def labelPatch(vecAll, imgParent,i):
    xc=vecAll[:,0].astype(np.float)+vecAll[:,3].astype(np.float)
    yc=vecAll[:,1].astype(np.float)+vecAll[:,4].astype(np.float)
    delta = 1.3*vecAll[:,2].astype(np.float)
    xr=(xc+delta).astype(np.int16)
    yr=(yc+delta).astype(np.int16)
    xl = (xc-delta).astype(np.int16)
    yl = (yc-delta).astype(np.int16)
    plt.imshow(imgParent[yl[i]:yr[i],xl[i]:xr[i],:])
    return [xl,yl,xr,yr]



    



