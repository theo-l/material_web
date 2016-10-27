# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

# 权限验证相关机制
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from material.models import  Material

# Create your views here.
def login(request):
    return render(request,'registration/login.html')

def logout(request):
    pass

@login_required
def index(request):
    return HttpResponse("User Logged in")

#LoginRequiredMixin,
class MaterialListView( ListView):
    model=Material


