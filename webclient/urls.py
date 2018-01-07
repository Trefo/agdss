from django.conf.urls import url, include
from webclient import views as views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
                  #Page URLs
    path('', views.index, name='label_index'),
    path('label', views.label, name='label'),
    path('results', views.results, name='results'),
    path('view_label', views.view_label, name='view_label'),

    #GET/POST URLs

    #path('purge$', views.purge),
    path('addImage', views.addImage),
    path('cleanUpAndFixImages', views.cleanUpAndFixImages),
    path('updateImage', views.updateImage),
    path('getInfo', views.getInfo),
    path('getNewImage', views.getNewImage),
    path('convertAll', views.convertAll),
    path('unlabeledImages', views.unlabeledImages),
    path('numImageLabels', views.numImageLabels),
    path('combineAllImages', views.combineAllImages),
    path('calculateEntropyMap', views.calculateEntropyMap),
    path('applyLabels', views.applyLabels),
    path('loadLabels', views.loadLabels),
    path('fix_label_location', views.fix_label_location),
    path('print_label_data', views.print_label_data),
    path('get_overlayed_image/(<image_label_id>[0-9]*)', views.get_overlayed_image),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
