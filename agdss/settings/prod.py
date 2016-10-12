from agdss.settings.common import *


#Note: Include a '/' at end of folder names
STATIC_ROOT = "/home/jdas/Dropbox/Research/UPenn/kumar-prec-ag/"
LABEL_FOLDER_NAME='labels/'
LABEL_AVERAGE_FOLDER_NAME='averages/'
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG=False

