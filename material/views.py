# encoding:utf-8

# http-related libs
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# views-related libs
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# authenticate-related libs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# message-related libs
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# model-related libs
from material.models import Material, InMaterial, OutMaterial

#form related libs
from material.forms import (
        LoginUserForm, MaterialForm, MaterialFileForm, RegisterUserForm
    )

#helper-related libs
from material import utils

############################################################
# Create your views here.
############################################################

def login(request):
    # 登录视图

    # 未登录时 为匿名用户对象
    user = request.user

    if request.method == 'POST':

        # 定义登录后跳转重定向 URL
        next_url = request.POST['next'] if 'next' in request.POST else '/'

        # 根据请求对象来构建 数据绑定之后的表单对象
        form = LoginUserForm(request.POST)
        
        #验证表单数据，会调用 errors()方法，errors()会调用full_clean():依次又调用_clean_fields(),_clean_form(),_post_clean()
        if form.is_valid():

            # 使用django提供的 auth 应用来验证登录用户
            user = authenticate(
                        username=form.cleaned_data['username'], 
                        password=form.cleaned_data['password']
                    )

            if user is not None:
                # 使用 auth 应用来登录用户，该方法会将登录的用户绑定到session/cookie中
                auth_views.login(request, user)
                # 登录成功后重定向
                return redirect(next_url)
            else:
                # 当验证用户失败之后，在登录页面表单中写入错误消息
                form.add_error(None, '用户名与密码不匹配!')
    else:
        # 表单初始化填充数据
        form_initial_data = {
            'username': '用户名'
        }
        # 构建数据未绑定的表单对象
        form = LoginUserForm(initial=form_initial_data)

        # 访问表单对象的字段并修改其选项值
        form.fields['username'].label = 'Username'
        next_url = request.GET['next'] if 'next' in request.GET else "/"

    # 通过模板以及上下文数据对象来渲染请求页面给用户
    return render(request, 'registration/login.html', {'form': form, 'next': next_url, 'user': user})



def register(request):
    # 用户注册视图

    if request.method == "POST":

        form = RegisterUserForm(request.POST)
        # 表单数据验证
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.save()
            # 使用消息框架来显示用户操作结果信息
            messages.add_message(request, messages.SUCCESS, "Register succeed")
            return redirect(reverse('index'))
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def logout(request):
    # 用户登出视图

    #使用 auth 应用提供的logout 方法来注销用户对象
    auth_views.logout(request)
    return redirect(reverse('index'))


def password_reset(request):
    'password reset view method'
    return HttpResponse('Reset Password! Enter your email')

############################################################
# 错误视图处理，需要设置 DEBUG=False 生效
############################################################

def page_not_found(request):
    # 处理页面未找到的404错误
    return render(request, 'material/404.html')


# @login_required
def index(request):
    'index view'
    return render(request, 'material/index.html')

########################################################
# Material-related operations
########################################################


@login_required
def material_add(request):
    #新建材料对象

    if request.method == 'POST':
        #使用ModelForm来处理
        form = MaterialForm(request.POST)

        if form.is_valid():
            material = form.save()

            if material.id is not None:
                messages.add_message(request, messages.INFO, "Material create success")
                return redirect(reverse('material-detail', args=[material.id]))

            else:
                messages.add_message(request, messages.WARNING, "Material already exists in database")
    else:
        form = MaterialForm()

    return render(request, 'material/material/material_add.html', {'form': form})


@login_required
def material_import(request):

    if request.method == 'POST':
        print "uploading file..."
        form = MaterialFileForm(request.POST, request.FILES)

        if form.is_valid():
            print "uploading form is valid..."

            import_file = request.FILES['file']
            utils.material_file_process(import_file)

            # message in views
            messages.add_message(request, messages.SUCCESS, "File Imported Success")

            # process uploaded file objects
            return redirect(reverse('material-index'))

    else:
        form = MaterialFileForm()

    return render(request, 'material/material/material_import.html', {'form': form})


@login_required
def material_list(request):

    key = None

    if request.method == 'POST':
        key = request.POST['key']

        if key is not None:
            material_list = Material.objects.filter(name__icontains=key)
        else:
            material_list = Material.objects.all()

    else:
        material_list = Material.objects.all()

    if key is None:
        key = ""

    # 使用分页对象对对象列表进行分页控制处理
    paginator = Paginator(material_list, 20)

    # 获取GET的查询值
    page = request.GET.get('page')
    try:
        materials = paginator.page(page)
    except PageNotAnInteger:
        materials = paginator.page(1)
    except EmptyPage:
        materials = paginator.page(paginator.num_pages)

    return render(request, 'material/material/material_list.html', {'materials': materials, 'key': key})


@login_required
def material_delete(request, pk=None):

    material = get_object_or_404(Material, pk=pk)
    material_name=material.name
    material.delete()
    messages.add_message(request, messages.INFO,'材料:%s删除成功'%material_name)
    return redirect(reverse('material-index'))



#使用基于类的更新视图更好控制一些
class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    context_object_name = 'material'
    fields = "__all__"
    template_name = 'material/material/material_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.add_message(request, messages.SUCCESS, "Material Update Succeed!")
        return super(MaterialUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('material-detail', args=[self.object.id])





############################################################
# 材料入库相关视图，将会采用基于类的视图来处理各个操作
# TODO 使用view-function 来实现一个更新视图
############################################################
class InMaterialListView(LoginRequiredMixin, ListView):

    model = InMaterial
    template_name = 'material/inmaterial/inmaterial_list.html'

    def get(self, request, *args, **kwargs):
        print "InMaterial get request"
        return super(InMaterialListView, self).get(request, *args, **kwargs)



############################################################
# 材料出库相关视图，将会采用基于类的视图来处理各个操作
############################################################
class OutMaterialListView(LoginRequiredMixin, ListView):
    model = OutMaterial
    template_name = 'material/outmaterial/outmaterial_list.html'

