#!/usr/bin/python
# encoding:utf-8
"project's form module"

from django import forms

from material.models import (
    Material, InMaterial, OutMaterial
)


class LoginUserForm(forms.Form):

    '''
    Login user field accept form
    '''

    username = forms.CharField(
        label='User Name', max_length=100, initial='username')  #
    password = forms.CharField(
        label='Password', max_length=20, widget=forms.PasswordInput)

    ############################################################
    # form 的自身属性
    ############################################################

    # 改变 form 在模板上进行渲染时的各个字段顺序。
    field_order = ['username', 'password']  # default=None

    # 字段标签名称的后缀
    label_suffix = '=>'  # default=':'

    # 字段的id属性以及字段label的 for属性
    auto_id = 'for_%s'  # default='id_%s' %s 被字段名称替换

    # 指定 form 字段在模板中渲染使用的样式

    required_css_class = 'required'
    error_css_class = 'error'

    ############################################################
    # form 的自身的一些特殊方法
    ############################################################
    def clean(self):
        """
        该方法中我们可以添加表单字段的定制验证器
        """
        print "定制的表单字段验证器"

        super(LoginUserForm, self).clean()
        username = self.cleaned_data['username']

        if username == 'test':
            # 为表单的某个字段添加 error 信息
            self.add_error('username', "Username can not be a test user")


class RegisterUserForm(forms.Form):
    email = forms.EmailField(max_length=50, strip=True)
    username = forms.CharField(max_length=20, min_length=5, strip=True, label="User Name")
    password = forms.CharField(label="Password", max_length=20, strip=True, widget=forms.PasswordInput)
    repassword = forms.CharField(label="Confirm Password", max_length=20, strip=True, widget=forms.PasswordInput)


class MaterialFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = '__all__'  # exclude=[]

    def clean(self):
        self._validate_unique = False
        return self.cleaned_data
