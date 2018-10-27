from django.conf.urls import url
from . import views

app_name = 'webclient'

urlpatterns= [
    url(r'^$', views.login_user, name="index1"),
    url(r'^index$', views.index, name="index"),
    url(r'^register/$', views.UserFormView.as_view(), name="register"),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^(?P<folder_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'folder/(?P<folder_id>[0-9]+)/add/$', views.create_folder, name="folder_add"),
    # url(r'ofile/add/$',views.OFileCreate.as_view(),name="ofile_add"),
    url(r'file/(?P<folder_id>[0-9]+)/add/$', views.create_file, name="file_add"),
    url(r'folder/(?P<pk>[0-9]+)/$', views.update_folder.as_view(), name="folder_update"),
    url(r'folder/(?P<pk>[0-9]+)/update/$', views.update, name="add_folder"),
    # url(r'ofile/(?P<pk>[0-9]+)/$',views.OFileUpdate.as_view(),name="ofile_update"),
    url(r'file/(?P<pk>[0-9]+)/$', views.FileUpdate.as_view(), name="file_update"),
    url(r'folder/(?P<pk>[0-9]+)/delete/$', views.delete_folder, name="folder_delete"),
    # url(r'ofile/(?P<pk>[0-9]+)/delete/$',views.OFileDelete.as_view(),name="ofile_delete"),
    url(r'file/(?P<pk>[0-9]+)/delete/$', views.FileDelete.as_view(), name="file_delete"),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]