# coding: utf-8

# 测试非 ORM 数据资源
import riak

# RESTful 相关的库
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, Resource

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

    # full=True 用来显示 User 的全部字段
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'  # 用来定义资源访问时 url 中的名称
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        # fields = ['title', 'pub_date', 'body']  # 限定资源访问时的字段
        # excludes=[...] # 去掉字段列表在资源访问时访问

#------------------------------------------------------------
        # get: 用来查询资源
        # post: 用来创建资源
        # put: 用来更新一个已经存在的资源或者更新整个资源集合数据
        # patch: 用来更新资源的部分信息
        # delete: 用来删除资源数据
        # 限定允许资源访问的方法, 用于限定资源访问可用的方法
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
#------------------------------------------------------------


class RiakObject:

    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class MessageResource(Resource):

    uuid = fields.CharField(attribute='uuid')
    user_uuid = fields.CharField(attribute='user_uuid')
    message = fields.CharField(attribute='message')
    created = fields.IntegerField(attribute='created')

    class Meta:
        resource_name = 'riak'
        object_class = RiakObject
        authorization = Authorization()

    def _client(self):
        return riak.RiakClient()

    def _bucket(self):
        client = self._client()
        return client.bucket('message')

    #============================================================
    # 以下 9 个方法用来实现任意资源的 RESTful API的实现
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    def get_object_list(self, request):
        query = self._client().add('messages')
        query.map(
            "function(v){var data = JSON.parse(v.values[0].data); return [[v.key,data]]}")
        results = []

        for result in query.run():
            new_obj = RiakObject(initial=result[1])
            new_obj.uuid = result[0]
            results.append(new_obj)

        return results

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        bucket = self._bucket()
        message = bucket.get(kwargs['pk'])
        return RiakObject(initial=message.get_data())

    def obj_create(self, bundle, **kwargs):
        bundle.obj = RiakObject(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        bucket = self._bucket()
        new_message = bucket.new(bundle.obj.uuid, data=bundle.obj.to_dict())
        new_message.store()
        return bundle

    def obj_update(self, bundle, **kwargs):
        return self.obj_create(bundle, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        bucket = self._bucket()

        for key in bucket.get_keys():
            obj = bucket.get(key)
            obj.delete()

    def obj_delete(self, bundle, **kwargs):
        bucket = self._bucket()
        obj = bucket.get(kwargs['pk'])
        obj.delete()

    def rollback(self, bundles):
        pass
    #============================================================
