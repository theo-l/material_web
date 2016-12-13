# encoding: utf-8
"""material_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin

from material.views import index, login, password_reset


from tastypie.api import Api
from material.api.resources import MaterialResource
from tastypie_test.api.resources import EntryResource, UserResource

# 定义一个Api对象来创建RESTful访问接口
v1_api = Api(api_name='v1') # api_name 用来定义访问URL中的名称
# 将之前定义的RESTful访问子资源对象注册
v1_api.register(MaterialResource())
v1_api.register(EntryResource())
v1_api.register(UserResource())

#from django.contrib.auth import views as auth_views

urlpatterns = [
#    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'api/', include(v1_api.urls)),
    url(r'', include('material.urls')),
]
