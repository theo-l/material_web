# encoding:utf-8
from __future__ import unicode_literals

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Base(models.Model):

    create_time=models.DateTimeField(auto_now_add=True) #auto_now_add 在对象第一次创建时自动设置为当前时间
    last_update_time=models.DateTimeField(auto_now=True) #auto_now在每次对象保存时自动设置为当前时间

    class Meta:
        abstract = True


class Material(Base):
    name=models.CharField(max_length=50)
    type_no=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    count=models.IntegerField(default=0)
    unit=models.CharField(max_length=20)
    note=models.CharField(max_length=100, blank=True)

    class Meta:
        db_table='material'
        ordering=['create_time']
        get_latest_by='create_time' # this option will affect QuerySet's latest()/earliest()

    @staticmethod
    def new_(name, type_no, price=0.0, count=0, unit='za', note=''):
        return Material(name=name, type_no=type_no, price=price, count=count, unit=unit, note=note)

    def __str__(self):
        return "%s - %s" %(self.name, self.type_no)

class InMaterial(Base):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    count=models.IntegerField(default=0)

        
    class Meta:
        db_table='in_material'
        default_related_name='ins'
        ordering=['-create_time']

    @staticmethod
    def new_( user, material, count=0):
        return InMaterial(user=user, material=material,count=count)

    def __str__(self):
        return self.user.username +" - "+self.material.name

class OutMaterial(Base):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    count=models.IntegerField(default=1)
    usage=models.CharField(max_length=100, blank=True)

    class Meta:
        db_table='out_material'
        default_related_name='outs'
        ordering=['-create_time']

    @staticmethod
    def new_(user, material, count=0, usage=''):
        return OutMaterial(user=user, material=material, count=count, usage=usage)

    def __str__(self):
        return self.user.username +" - "+self.material.name
