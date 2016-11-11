#!/usr/bin/python
# encoding:utf-8

"""
File: signals.py
Author: theo-l
Email: yourname@email.com
Github: https://github.com/theo-l
Description: 应用中的所有信号处理器定义文件
"""

from django.db.models.signals import pre_save
from django.core.signals import request_finished
from django.dispatch import receiver
from material.models import OutMaterial, InMaterial

'''
###########################################################
 信号相关的使用
----------------------------------------------------------
 1. 信号的定义

        所有的信号都是 django.dispatch.Signal 类的实例。
        通过 providing_args 参数来提供为信号接收函数所
        使用的参数。该方式只是文档声明的，无法检查信号
        是否真正地提供了这些参数

        signal_name = Signal(providing_args=['topping','size'])

 2. 信号的接收函数

       - 信号的接收函数可以是任意的Python函数或方法，其参数列表必须如下

        def signal_handler(sender, **kwargs):
            pass

 3. 绑定信号与接收函数
        - 有两种方式来将信号与接收函数绑定

            1. 通过信号自身的connect()函数来绑定接收函数
                signal_instance.connect(signal_receiver_function)

            2. 对信号接收函数上使用 @receiver()装饰器

                @receiver(signal_name[,sender])
                def signal_handler(sender,**kwargs):
                    pass


 4. 信号的发送

        有两种方式来发送信号

        1. Signal.send(sender, **kwargs)
        2. Signal.send_robus(sender, **kwargs)

 5. 信号接收函数的定义代码的所在位置

        通常在signals子模块中定义所有的信号处理器，然后在 apps 中的 ready()
        方法中导入该 signals 子模块

 6. 防止信号重复绑定信号接收函数

        通过使用dispatch_uid参数，signal_name.connect(signal_receiver_function, dispatch_uid='string_value')
        来使得信号接收函数与每个唯一的 dispatch_uid 绑定一次。

7. 断开信号与信号接收函数之间的绑定

    Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)


###########################################################


###########################################################
 内置的信号集合

----------------------------------------------------------
 1. model 相关的信号(django.db.models.signals 定义了由 model 系统发出的信号集)

   - pre_init
           (sender, args, kwargs)
   - post_init
           (sender, instance)
   ========这两个信号是在 model 实例化一个 model 的前后发出的

   - pre_save(sender, instance, created, raw, using, update_fields)
   - post_save(sender, instance, created, raw, using, update_fields)
   ========这两个信号是在 model 实例调用 save() 的前后发出的

   - pre_delete(sender, instance, using)
   - post_delete(sender, instance, using)
   ========这两个信号是在 model 实例或queryset 实例调用 delete() 方法前后发出的

   - m2m_changed(sender, instance, action=['pre_add','post_add','pre_remove','post_remove','pre_clear', 'post_clear'], reverse, model, pk_set, using)
   ========当一个model实例上的一个 ManyToManyField 更新之后发出的

   - class_prepared
   ========当一个model定义并注册到django的model系统之后发出的


------------------------------------------------------------
 2. management 相关的信号

   - pre_migrate(sender, app_config, verbosity, interactive, using, plan, apps)
   - post_migrate(sender, app_config, verbosity, interactive, using, plan, apps)
   ========由 migrate 命令执行前后发出的，对于没有 models 模块的应用不会触发。

------------------------------------------------------------
 3. request/response 相关的信号

   - request_started(sender, environ)
   - request_finished(sender)
   ========在django处理一个HTTP请求的前后发出的

   - got_request_exception(sender, request)
   ========在django处理一个到来的HTTP请求发现异常时发出的。


------------------------------------------------------------
 4. test 相关的信号, 运行测试时发出的

   - setting_changed(sender, setting, value, enter)
   =======当通过 django.test.TestCase.settings() 上下文管理器更新setting的值时发出的信号

   - template_rendered(sender, template, context)
   ========当测试系统渲染一个模板时发出的， 在正常模式下不触发该信号。


------------------------------------------------------------
 5. 数据库包装器信号

   - connection_created(sender, connection)
   ========在一个数据库连接初始化之后发出的信号

##########################################################
'''

############################################################
# 在此定义你的信号处理器函数
############################################################
# model pre_save signal handler
@receiver(pre_save, sender=OutMaterial)
def outmaterial_pre_save_handler(sender, **kwargs):
    obj = kwargs['instance']
    print("OutMaterial before save, Count: %s" % obj.count)
    # material = obj.material
    # material.count -= obj.count
    # material.save()


@receiver(pre_save, sender=InMaterial)
def inmaterial_pre_save_handler(sender, **kwargs):
    obj = kwargs['instance']
    print("InMaterial before save, Count: %s" % obj.count)
    # material = obj.material
    # material.count += obj.count
    # material.save()
# request finished signal handler


@receiver(request_finished)
def request_end(sender, **kwargs):

    print "Request finished", kwargs
