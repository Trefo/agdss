from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Page URLs
    url(r'^$', views.index, name='index'),
    url(r'^label$', views.label, name='label'),
    url(r'^results$', views.results, name='results'),
    url(r'^view_label$', views.view_label, name='view_label'),

    #GET/POST URLs
    url(r'^applyLabels$', 'webclient.views.applyLabels'),
    url(r'^loadLabels$', 'webclient.views.loadLabels'),
    url(r'^purge$', 'webclient.views.purge'),
    url(r'^addImage$', 'webclient.views.addImage'),
    url(r'^updateImage$', 'webclient.views.updateImage'),
    url(r'^getInfo$', 'webclient.views.getInfo'),
    url(r'^getNewImage$', 'webclient.views.getNewImage'),
    url(r'^convertAll$', 'webclient.views.convertAll'),
    url(r'^unlabeledImages$', 'webclient.views.unlabeledImages'),
    url(r'^numImageLabels$', 'webclient.views.numImageLabels'),
    url(r'^combineAllImages$', 'webclient.views.combineAllImages'),
    url(r'^calculateEntropyMap$', 'webclient.views.calculateEntropyMap'),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)