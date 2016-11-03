# encoding:utf-8
from django.contrib import admin

from material.models import (
    Material, InMaterial, OutMaterial
)

# Register your models here.
# Let application's model can be managed by admin site


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    ########################################
    # ModelAdmin options list

    # model 列表页面中可操作的列表
    actions = []

    # 控制 actions 列表在页面中显示的位置
    actions_on_top = True
    actions_on_bottom = False

    # 控制是否在actions的旁边显示选择计数器
    actions_selection_counter = True

    # 指定一个日期/时间字段来控制包含一个依赖该字段的基于日期的导航
    date_hierarchy = 'create_time'

    # 重载model字段的默认空值在页面中的显示方式
    empty_value_display = '-empty-'

    # 控制在页面显示中应该排除的字段列表
    exclude = ()

    # 控制在页面显示中应该包含的字段列表
    # fields=()

    # 用来控制admin页面中的add/change的布局方式, 是一个二元组数据对象列表(name, field_options)
    #    fieldsets=(
    #                (
    #                    None,
    #                    {
    #                        'fields':()
    #                    }
    #                ),
    #                (
    #                    'Advanced options',
    #                    {
    #                        'fields':(),
    #                        'classes':(),
    #                        'description':string-value
    #                    }
    #                )
    #            )

    # 控制过滤器显示的方式
    # filter_horizontal/filter_vertical

    # 为ModelAdmin指定自定义的ModelForm对象来替换默认创建的form
    # form

    # 提供了一个快速但脏的方式来在admin中重载一些Field的选项,用来重载渲染样式等
    # formfield_overrides = {
    #         models.TextField:{'widget': RichTextEditorWidget}
    #         }

    # inlines

    # 控制在admin的列表页面显示字段的列表元组,如果未指定则显示__str__()的返回值
    list_display = ('name', 'type_no', 'price', 'count', 'unit', 'note')

    # 控制在页面显示的对象列表中对哪些字段添加链接
    list_display_links = ('name', 'type_no')

    # 控制在对象列表显示页面可直接编辑的字段
    # list_editable=('note',)

    # 控制在对象列表页面的右边显示指定字段列表的过滤器列表
    list_filter = ('name', 'create_time')

    # 控制多少个对象可以显示"show all"链接
    list_max_show_all = 50

    # 控制对象列表页面每页显示对象的个数
    list_per_page = 25

    # 控制对象列表页中显示对象的相关联对象
    # list_select_related

    # 控制对象列表的排序方式
    ordering = ('name',)

    # 指定页面分页器类， 默认为django.core.paginator.Paginator
    # paginator=

    # 一个字段名称到其应该预先加载自的字段映射对象
    # prepopulated_fields={
    #         'note':("name",)
    #         }

    # admin会在创建，编辑或删除一个对象后保留过滤器，通过设置为False可以回复清理过滤器的行为
    # preserve_filters=True/False

    # 为 Foreignkey或具有 choices 选项的字段使用单选按钮来进行渲染
    # radio_fields={'field_name':admin.VERTICAL}

    # raw_id_fields

    # 将指定的字段渲染为只读字段, 这样就不可编辑
    readonly_fields = ('count',)

    # 默认django提供了三种保存方式: 保存、保存并继续编辑、保存并增加一个新的
    # save_as 会将对象作为一个新的对象保存
    save_as = False

    # 如果为Flase， 当save_as=True时，保存之后会跳转到对象列表页面
    save_as_continue = True

    # 在对象列表上面添加一个保存按钮
    save_on_top = False

    # 会在对象列表上方添加一个搜索框， 在指定的字段中进行过滤
    # 可以在字段名中添加一些修饰符来加快或者限定搜索:
    # ^: startswith
    # =: exact
    # @: contains
    search_fields = ['name', 'type_no']

    # 控制是否显示全部结果的计数器
    show_full_result_count = True

    view_on_site = True

    # 以下选项用来定制admin中使用的模板
    # add_form_template
    # change_form_template
    # change_list_template
    # delete_confirmation_template
    # delete_selected_confirmation_template
    # object_history_template
    ########################################


@admin.register(InMaterial)
class InMaterialAdmin(admin.ModelAdmin):

    list_display = ('user', 'material', 'count',)
    list_display_links = ('user', 'material')
    list_select_related = True

    search_fields = ('user__username', 'material__name', 'material__type_no')
    list_filter = ('user',)


@admin.register(OutMaterial)
class OutMaterialAdmin(admin.ModelAdmin):

    list_display = ('user', 'material', 'count', 'usage')
    list_display_links = ('user', 'material')
    list_select_related = True

    search_fields = ('user__username', 'material__name', 'material__type_no')
	# list_display=('user__username','material__name', 'material__type_no','count', 'usage')
    list_filter = ('user',)

    # def save_model(self, request, obj, form, change):
    #     print "Material count:", obj.material.count
    #     print "Out Count", form.cleaned_data['count']

    #     if obj.material.count < form.cleaned_data['count']:
    #         print "out count is greater than exist count"
    #         self.message_user(request, "出库量大于库存量，出库失败!")
