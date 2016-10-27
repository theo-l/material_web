#!/usr/bin/python
# encoding:utf-8

from django.conf.urls import url
from material.views import index, MaterialListView

urlpatterns=[
        url(r'^$', index),

        # /material/list/
        url(r'^list/$', MaterialListView.as_view()),

        ]
