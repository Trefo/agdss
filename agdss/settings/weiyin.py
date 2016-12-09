from agdss.settings.common import *

#Note: Include a '/' at end of folder names
STATIC_ROOT = "/mnt/c/Users/weiyi/Documents/AgLabImgs"
LABEL_FOLDER_NAME='temp/'
LABEL_AVERAGE_FOLDER_NAME='temp_averages/'
SECRET_KEY = 'q82m6os5(_m4s7tabkfsz1y90dsnz1q(_c^+u&zs+ffftgs*2$'
#Filepath for user uploaded images
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
HOST_ROOT = 'http://localhost:8000'
# print BASE_DIR
# print MEDIA_ROOT
