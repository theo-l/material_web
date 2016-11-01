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

from material.models import Material, InMaterial, OutMaterial
from material.forms import (
    LoginUserForm, MaterialForm, MaterialFileForm, RegisterUserForm
)
from material import utils

# Create your views here.
# TODO


def login(request):
    'login view'

    user = request.user

    if request.method == 'POST':
        print request.POST['next']
        next_url = request.POST['next'] if 'next' in request.POST else '/'
        form = LoginUserForm(request.POST)

        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                auth_views.login(request, user)
                return redirect(next_url)
            else:

                form.add_error(None, '用户名与密码不匹配!')
    else:

        form_initial_data = {
            'username': '用户名'
        }
        form = LoginUserForm(initial=form_initial_data)

        form.fields['username'].label = 'Username'
        next_url = request.GET['next'] if 'next' in request.GET else "/"

    return render(request, 'registration/login.html', {'form': form, 'next': next_url, 'user': user})

# TODO


def register(request):

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', "Username already exists!")
            elif form.cleaned_data['password'] != form.cleaned_data['repassword']:
                # messages.add_message(request, messages.WARNING, "Two passwords are not compatible!")
                form.add_error('repassword', 'Two passwords are not compatible!')
            else:
                user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
                user.save()
                messages.add_message(request, messages.SUCCESS, "Register succeed")
                return redirect(reverse('index'))
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def logout(request):
    'logout view method'
    auth_views.logout(request)
    return redirect(reverse('index'))


def password_reset(request):
    'password reset view method'
    return HttpResponse('Reset Password! Enter your email')


def page_not_found(request):
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

    if request.method == 'POST':
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

    paginator = Paginator(material_list, 20)

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

    print "Deleting pk=%s" % pk
    material = get_object_or_404(Material, pk=pk)
    material.delete()
    return redirect(reverse('material-index'))


@login_required
def material_detail(request, pk=None):
    print "Detaling pk=%s" % pk
    material = get_object_or_404(Material, pk=pk)

    form = MaterialForm(instance=material)

    return render(request, 'material/material/material_detail.html', {'form': form, 'material': material})


class MaterialListView(LoginRequiredMixin, ListView):

    #    model = Material
    #    queryset=Material.objects.order_by('-create_time')

    context_object_name = 'materials'

    template_name = 'material/material/material_list.html'

    def get(self, request):
        print "material list view"
        return render(request, self.template_name)

    # 动态过滤模板中的对象列表数据
    def get_queryset(self):

        return Material.objects.order_by('-create_time')


class MaterialDetailView(LoginRequiredMixin, DetailView):

    model = Material  # queryset = Material.objects.all()
    context_object_name = 'material'

    # 为模板中添加额外的对象
    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        return context

    # 为获取到的对象执行额外的操作
    def get_object(self, *args, **kwargs):
        obj = super(MaterialDetailView, self).get_object(*args, **kwargs)
        # 可以对object 执行额外的操作
        return obj


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'type_no', 'price', 'count', 'unit', 'note']
    template_name = 'material/material/material_form.html'


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


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material


# TODO


class InMaterialListView(LoginRequiredMixin, ListView):

    model = InMaterial
    template_name = 'material/inmaterial/inmaterial_list.html'

    def get(self, request, *args, **kwargs):
        print "InMaterial get request"
        return super(InMaterialListView, self).get(request, *args, **kwargs)

# TODO


class OutMaterialListView(LoginRequiredMixin, ListView):
    model = OutMaterial
    template_name = 'material/outmaterial/outmaterial_list.html'
