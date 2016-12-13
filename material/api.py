# -*- coding: utf-8 -*-

from tastypie.resources import ModelResource
from .models import Material

class MaterialResource(ModelResource):
    class Meta:
        queryset = Material.objects.all()