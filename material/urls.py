#!/usr/bin/python
# encoding:utf-8

from django.conf.urls import url

from material import views

urlpatterns = [

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),

    url(r'^$', views.index, name='index'),

    # Material urls configs
    url(r'^material/$', views.material_list, name='material-index'),
    url(r'^material/import/$', views.material_import, name='material-import'),

    url(r'^material/add/$', views.material_add, name='material-add'),

    url(r'^material/update/(?P<pk>[0-9]+)/$',
        views.MaterialUpdateView.as_view(), name='material-update'),

    url(r'^material/delete/(?P<pk>[0-9]+)/$',
        views.material_delete, name='material-delete'),

    # InMaterial url configs
    url(r'^inmaterial/$', views.InMaterialListView.as_view(),
        name='inmaterial-index'),

    # OutMaterial url configs
    url(r'^outmaterial/$', views.OutMaterialListView.as_view(),
        name='outmaterial-index'),
]
