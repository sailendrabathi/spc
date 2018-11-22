"""spc1 URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from webclient import views

import webclient

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^webclient/', include('webclient.urls')),
    url(r'^files/', include('db_file_storage.urls')),
    url(r'^apiregister/',views.register.as_view(),name='api_register'),
    url(r'^apilogin/',views.loginapi.as_view(),name='api_login'),
    url(r'^apiauth/',views.authapi.as_view(),name='api_auth'),
    url(r'^apilogout/',views.logoutapi.as_view(),name="api_logout"),
    url(r'^fileuploadapi/',views.fileuploadapi.as_view(),name='api_file'),
    url(r'folderuploadapi/',views.folderuploadapi.as_view(),name='folderuploadapi'),
    url(r'^apishowdata/',views.showdataapi.as_view(),name = 'showdataapi'),
    url(r'^filedeleteapi/',views.filedeleteapi.as_view(),name='filedeleteapi'),
    url(r'^folderdeleteapi/',views.folderdeleteapi.as_view(),name='folderdeleteapi'),
    url(r'^apidownloadfolder/',views.folderdownloadapi.as_view(),name='folderdownloadapi'),
    url(r'^apidownloadfile/',views.filedownloadapi.as_view(),name='filedownloadapi'),
    url(r'^apisync/',views.apisync.as_view(),name='filedownloadapi'),
    url(r'^apiupdate/',views.apiupdate.as_view(),name='updateapi'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
