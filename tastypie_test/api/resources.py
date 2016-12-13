# coding: utf-8

# RESTful 相关的库
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

# Django 中的数据
from django.contrib.auth.models import User

# 当前项目中的 models
from tastypie_test.models import Entry


# 基于 Django 的Model来创建一个 RESTful 访问资源对象
class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        filtering = {
            'username': ALL,
        }
        excludes = [
            'email', 'password', 'is_active', 'is_staff', 'is_superuser']


class EntryResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user', full=True) # full=True 用来显示 User 的全部字段

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'  # 用来定义资源访问时 url 中的名称
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
#         fields = ['title', 'pub_date', 'body']  # 限定资源访问时的字段
        # excludes=[...] # 去掉字段列表在资源访问时访问
        allowed_methods = ['get','post','put','patch','delete']  # 限定允许资源访问的方法, 用于限定资源访问可用的方法
