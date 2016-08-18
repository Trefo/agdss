"""agdss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
import django.views

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView
from django.contrib import admin
from adminplus.sites import AdminSitePlus


#Set up admin site and import all admin.py files
admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()



urlpatterns = [
    url(r'^webclient/', include('webclient.urls')),
    url(r'^admin/', admin.site.urls),


    url('^', include('django.contrib.auth.urls')),

    url('^register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url= '/login'
    )),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^$', RedirectView.as_view(url='/webclient/')),

]
