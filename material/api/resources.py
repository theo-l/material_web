# -*- coding: utf-8 -*-

from tastypie.resources import ModelResource
from material.models import Material

class MaterialResource(ModelResource):
    class Meta:
        queryset = Material.objects.all()
        allowed_methods = ['get']