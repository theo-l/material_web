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
