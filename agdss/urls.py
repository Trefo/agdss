"""agdss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
import django.views
from django.urls import include, path

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
    path('webclient/', include('webclient.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url= '/login'
    )),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/webclient/')),

]
