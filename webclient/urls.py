from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^applyLabels$', 'webclient.views.applyLabels'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)