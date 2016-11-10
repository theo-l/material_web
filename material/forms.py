#!/usr/bin/python
# encoding:utf-8
"project's form module"

from django import forms

from material.models import (
    Material, InMaterial, OutMaterial
)

from django.contrib.auth.models import User


def debug(message):
    print(" ".join(["=" * 20, " %s ", "=" * 20]) % message)


class LoginUserForm(forms.Form):

    '''
    普通的Form对象用来接收用户登录表单数据 
    '''

    username = forms.CharField(label='User Name', max_length=100, initial='username')

    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)

    ############################################################
    # form 的自身属性

    field_order = ['username', 'password']  # default=None 改变 form 在模板上进行渲染时的各个字段顺序。
    label_suffix = '=>'  # default=':' 字段标签名称的后缀
    auto_id = 'for_%s'  # default='id_%s' %s 被字段名称替换 字段的id属性以及字段label的 for属性
    #-------------------------------- 指定 form 字段在模板中渲染使用的样式
    required_css_class = 'required'
    error_css_class = 'error'
    ############################################################

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

    '''
        注册用户数据表单
    '''

    email = forms.EmailField(max_length=50, strip=True)
    username = forms.CharField(max_length=20, min_length=5, strip=True, label="User Name")
    password = forms.CharField(label="Password", max_length=20, strip=True, widget=forms.PasswordInput)
    repassword = forms.CharField(label="Confirm Password", max_length=20, strip=True, widget=forms.PasswordInput)

    # 定制表单数据字段的相关验证逻辑
    def clean(self):

        # 用户名的唯一性验证
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', "该用户名已经存在!")

        # 密码确认验证
        elif self.cleaned_data['password'] != self.cleaned_data['repassword']:
            self.add_error('repassword', "两次密码不相同")
        else:
            return super(RegisterUserForm, self).clean()


class MaterialFileForm(forms.Form):

    '''
    带文件字段的表单
    '''
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class MaterialForm(forms.ModelForm):

    '''
    ModelForm 使用 样例
    '''

    class Meta:
        # 指定ModelForm的相关Meta选项， 可以通过ModelForm实例的_meta 来访问
        model = Material
        fields = '__all__'
#        exclude=[]
#        widgets
#        localized_fields
#        labels
#        help_texts
#        error_messages
#       field_classes

    def clean(self):
        self._validate_unique = False
        return self.cleaned_data


class InMaterialForm(forms.ModelForm):

    """docstring for InmaterialForm"""

    class Meta:
        model = InMaterial
        fields = "__all__"

    def clean(self):
        'this method will be called when invoke is_valid()/errors'
        self.validate_in_count()
        return self.cleaned_data

    def validate_in_count(self):
        debug("Validating InMaterial Create Form")
        if self.cleaned_data['count'] <= 0:
            self.add_error('count', "Material In Count can not be <= 0")
            return
        material = self.cleaned_data['material']
        material.count += self.cleaned_data['count']
        material.save()


class OutMaterialForm(forms.ModelForm):

    class Meta:
        model = OutMaterial
        fields = "__all__"

    def clean(self):
        self.update_material_count()
        return self.cleaned_data

    def update_material_count(self):
        debug("Validating OutMaterial Create Form")
        material = self.cleaned_data['material']
        if self.cleaned_data['count'] <= 0:
            self.add_error('count', "Material Out Count can not be less than 0")
            return
        elif self.cleaned_data['count'] > material.count:
            self.add_error('count', "Material Out Number %s is over %s" % (self.cleaned_data['count'], material.count))
            return
        else:
            material.count -= self.cleaned_data['count']
            material.save()
