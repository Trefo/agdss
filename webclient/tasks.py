#Celery tasks
from __future__ import absolute_import

from celery import Celery, shared_task, Task
from webclient.image_ops import convert_images
from webclient.models import *

@shared_task
def task_convertSVG(label_id, reconvert=False):
    svg = convert_images.convertSVG(ImageLabel.objects.get(id=label_id), reconvert)
    return svg

@shared_task
def task_combineImageLabels(image_id, threshold):
    convert_images.combineImageLabels(Image.objects.get(id=image_id), threshold)
    return 0