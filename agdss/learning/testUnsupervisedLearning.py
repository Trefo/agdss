import cPickle

from PIL import Image
import numpy
image = Image.open('color.png', 'r').getdata()
imageArray = numpy.fromstring(image.tostring(), dtype='uint8', count=-1, sep='').reshape(image.shape + (len(image.getbands()),))


train_set_x = ''
train_set_y = ''


f = file('my_data.pkl', 'wb')
cPickle.dump((train_set_x, train_set_y), f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()

# CODE NOT COMPLETE