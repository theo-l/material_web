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
from material.models import OutMaterial



############################################################
# 在此定义你的信号处理器函数
############################################################
# model pre_save signal handler
@receiver(pre_save, sender=OutMaterial)
def outmaterial_pre_save_handler(sender, **kwargs):
    obj=kwargs['instance']
    print "==============saving OutMaterial with count: %s" % obj.count
    print kwargs

# request finished signal handler
@receiver(request_finished)
def request_end(sender, **kwargs):

    print "Request finished", kwargs
