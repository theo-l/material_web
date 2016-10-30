#!/usr/bin/python
# encoding:utf-8

from django.conf.urls import url
from material.views import *

urlpatterns = [
    url(r'login/$', login, name='login'),
    url(r'password_reset/$', password_reset, name='password_reset'),

    url(r'^$', index, name='index'),

    # Material urls configs
    url(r'material/$', MaterialListView.as_view(), name='material-index'),

    url(r'material/add/$', MaterialCreateView.as_view(), name='material-add'),

    url(r'material/update/(?P<pk>[0-9]+)/$',
        MaterialUpdateView.as_view(), name='material-update'),

    url(r'material/delete/(?P<pk>[0-9]+)/$',
        MaterialDeleteView.as_view(),	name='material-delete'),

    url(r'material/(?P<pk>[0-9]+)/$',
        MaterialDetailView.as_view, name='material-detail'),

    # InMaterial url configs
    url(r'inmaterial/$', InMaterialListView.as_view(),
        name='inmaterial-index'),

    # OutMaterial url configs
    url(r'outmaterial/$', OutMaterialListView.as_view(),
        name='outmaterial-index'),
]
