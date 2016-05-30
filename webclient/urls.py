from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Page URLs
    url(r'^$', views.index, name='index'),
    url(r'^results$', views.results, name='results'),

    #GET/PUSH URLs
    url(r'^applyLabels$', 'webclient.views.applyLabels'),
    url(r'^loadLabels$', 'webclient.views.loadLabels'),
    url(r'^purge$', 'webclient.views.purge'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)