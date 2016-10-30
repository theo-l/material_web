# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# 权限验证相关机制
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate

from material.models import Material, InMaterial, OutMaterial
from material.forms import LoginUserForm

# Create your views here.
# TODO


def login(request):
    'login view'

    # 默认的用户对象为  匿名用户
    user = request.user

    if request.method == 'POST':
        next_url = request.POST['next']
        # 从请求对象 request 来创建表单对象
        form = LoginUserForm(request.POST)

        # 验证表单数据
        if form.is_valid():

            # 访问表单对象时，通过 Form.cleaned_data 字典对象访问
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                auth_views.login(request, user)
                return redirect(next_url)
            else:

                # 为表单对象添加一个非字段错误消息，以便显示给用户其操作的结果
                #                form.add_error(None, 'username and password are not compatible!')
                form.add_error(None, '用户名和密码不匹配!')
    else:

        # 创建表单实例时使用的初始化数据
        form_initial_data = {
            'username': '用户名'
        }
        form = LoginUserForm(initial=form_initial_data)

        # 通过 Form.fields 属性可以访问Form中的每个字段实例
        form.fields['username'].label = 'Username'
        next_url = request.GET['next']

    return render(request, 'registration/login.html', {'form': form, 'next': next_url, 'user': user})

# TODO

 
def logout(request):
    'logout view method'
    return auth_views.logout(request)



def password_reset(request):
    'password reset view method'
    return HttpResponse('Reset Password! Enter your email')


@login_required
def index(request):
    'index view'
    return render(request, 'material/index.html')

# TODO
 
 
class MaterialListView(LoginRequiredMixin, ListView):

    model = Material
    template_name = 'material/material/material_list.html'

    def get(self, request):
        print "material list view"
        return render(request, self.template_name)


class MaterialDetailView(LoginRequiredMixin, DetailView):
 
    queryset = Material.objects.all()
    context_object_name = 'material'


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'type_no', 'price', 'count', 'unit', 'note']
    template_name = 'material/material/material_form.html'


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material


# TODO


class InMaterialListView(LoginRequiredMixin, ListView):

    model = InMaterial
    template_name = 'inmaterial/inmaterial_list.html'

# TODO


class OutMaterialListView(LoginRequiredMixin, ListView):
    model = OutMaterial
    template_name = 'outmaterial/outmaterial_list.html'
