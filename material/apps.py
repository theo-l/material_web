from __future__ import unicode_literals

from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import pre_save


class MaterialConfig(AppConfig):
    name = 'material'


    def ready(self):
        import material.signals
        super(MaterialConfig,self).ready()
