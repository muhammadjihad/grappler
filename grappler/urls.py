"""grappler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('graplearn/api/',include('graplearn.api.urls', namespace='graplearn-api')),
    path('akun/api/',include('akun.api.urls', namespace='akun-api')),
    path('grappost/',include('grappost.urls',namespace='grappost')),
    path('graplearn/',include('graplearn.urls', namespace='graplearn')),
    path('akun/',include('akun.urls', namespace='akun')),
    path('',views.index, name='home'),
    path('teruslahberjuang/', admin.site.urls),
    path('help/',include('help.urls', namespace='help'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Flixnote | Find Anything Learn Everything"
admin.site.site_title = "Flixnote | Find Anything Learn Everything"