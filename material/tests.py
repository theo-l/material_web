# -*- coding: utf-8 -*-
"""
File: tests.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description: 应用测试文件
"""

import datetime
from django.test import TestCase

from material.models import *

# Create your tests here.
class ModelTest(TestCase):

    def test_user_create(self):
        user=User(username='test', email='test@mail.com', password='testpassword')
        user.save()
        self.assertEqual(User.objects.get(username__exact='test'),user)

    def test_material_create(self):
        material=Material.new_('Fibra','12')
        material.save()
        self.assertSequenceEqual(Material.objects.all(),[material])

    def test_in_material_create(self):
        self.test_user_create()
        self.test_material_create()
        user=User.objects.get(username__exact='test')
        material=Material.objects.get(name__exact='Fibra')
        in_material = InMaterial.new_(user, material)
        in_material.save()
        self.assertEqual(InMaterial.objects.get(pk=1), in_material)

    def test_out_material_create(self):
        self.test_user_create()
        self.test_material_create()
        user=User.objects.get(username__exact='test')
        material=Material.objects.get(name__exact='Fibra')
        out_material=OutMaterial.new_(user,material)
        out_material.save()
        self.assertEqual(OutMaterial.objects.get(pk=1),out_material)


    def test_material_delete(self):
        self.test_material_create()
        material=Material.objects.all()[0]
        material.delete()
        self.assertSequenceEqual(Material.objects.all(),[])

    def test_material_create_time(self):
        "create time is now, last update time is seeted before save"
        material = Material.new_('Fibra','12')
        material.save()
        self.assertEqual(datetime.date.today(), material.create_time.date())
        self.assertGreater(material.last_update_time, material.create_time)

    def test_material_ordering(self):
        "material ordering by create_time asc"
        material_1=Material.new_('Fibra','11')
        material_2=Material.new_('Fibra','12')
        material_1.save()
        material_2.save()
        self.assertEqual(Material.objects.all()[0], material_1)

class QuerySetMethodTest(TestCase):

    def setUp(self):

        self.user=User(username='test', email='test@mail.com', password='testpassword')
        self.user.save()

        self.material=Material.new_('Fibra','12')
        self.material.save()

        self.material2=Material.new_('Fibra','24')
        self.material2.save()

        self.in_material=InMaterial.new_(self.user,self.material)
        self.in_material.save()

        self.in_material2 = InMaterial.new_(self.user,self.material2)
        self.in_material2.save()

        self.out_material=OutMaterial.new_(self.user,self.material)
        self.out_material.save()

        self.out_material2=OutMaterial.new_(self.user,self.material2)
        self.out_material2.save()

    def test_all(self):
        self.assertSequenceEqual(User.objects.all(),[self.user])
        self.assertSequenceEqual(Material.objects.all(),[self.material, self.material2])

        #InMaterial/OutMaterial orderred by create_time desc
        self.assertSequenceEqual(InMaterial.objects.all(),[self.in_material2,self.in_material])
        self.assertSequenceEqual(OutMaterial.objects.all(),[self.out_material2,self.out_material])

    def test_filter(self):
        self.assertSequenceEqual(Material.objects.filter(type_no='24'),[self.material2])

        self.assertSequenceEqual(Material.objects.filter(name__iexact='fibra',type_no='24'), [self.material2]) 
        self.assertSequenceEqual(InMaterial.objects.filter(material__name__iexact='fibra',material__type_no='24'),[self.in_material2])

        self.assertSequenceEqual(OutMaterial.objects.filter(material__name__iexact='fibra'),[self.out_material2,self.out_material])

    def test_exclude(self):

        self.assertSequenceEqual(Material.objects.exclude(type_no='24'),[self.material])

        self.assertSequenceEqual(Material.objects.exclude(name__iexact='fibra'),[])

        self.assertSequenceEqual(InMaterial.objects.exclude(material__type_no='24'),[self.in_material])

        self.assertSequenceEqual(OutMaterial.objects.exclude(material__name__iexact='fibra'),[])


    def test_order_by(self):
        '手动指定 QuerySet 的排序方式'
        # 按照创建时间升序排列
        self.assertSequenceEqual(InMaterial.objects.all().order_by('create_time'),[self.in_material,self.in_material2])

        '通过关联对象来指定当前model的排序方式'
        #Join material
        self.assertSequenceEqual(InMaterial.objects.order_by('material__id'), [self.in_material, self.in_material2])

        #Not join material
        self.assertSequenceEqual(InMaterial.objects.order_by('material_id'), [self.in_material, self.in_material2])

        # 按照创建时间升序排列
        self.assertSequenceEqual(OutMaterial.objects.all().order_by('create_time'),[self.out_material, self.out_material2])

    def test_reverse(self):
        self.assertSequenceEqual(InMaterial.objects.all().reverse(),[self.in_material, self.in_material2])
        self.assertSequenceEqual(OutMaterial.objects.all().reverse(),[self.out_material, self.out_material2])
        self.assertSequenceEqual(Material.objects.all().reverse(),[self.material2, self.material])

    def test_distinct(self):
        # distinct operation not supported by all database backend
        #self.assertSequenceEqual(Material.objects.all().distinct('name'),[self.material])
        pass
        
    def test_values(self):

        self.assertSequenceEqual(
                Material.objects.filter(type_no='24').values('id','name','type_no'),
                [{
                     'id':2,'name':'Fibra','type_no':'24' 
                 }]
                )

    def test_values_list(self):

        self.assertSequenceEqual(
               Material.objects.filter(type_no='24').values_list('id','name','type_no') ,
               [(2,'Fibra','24')]
                )
        
    def test_dates(self):
        #测试 dates()/datetimes() 具有相同的效果
        # datetimes具有一些额外的类型: hour, minute, second
        import datetime

        self.assertSequenceEqual(
               Material.objects.dates('create_time','year') ,
               [datetime.date(2016,1,1) ]
                )
        self.assertSequenceEqual(
               Material.objects.dates('create_time','month'),
               [datetime.date(2016,10,1)]
                )

        self.assertSequenceEqual(
               Material.objects.dates('create_time','day'), 
               [datetime.date.today()]
                )
        
    def test_none(self):
        
        self.assertSequenceEqual(
               Material.objects.none(),
               []
                )
        
    def test_select_related(self):
        # 将与model对象关联的对象从数据库中加载到python中以便之后的访问不需要再进行数据库访问。
        # select_related(*field)
        pass
        
    def test_prefetch_related(self):
        pass
        
        
    def test_extra(self):
        # 提供额外的数据库查询参数。
        self.assertSequenceEqual(
                Material.objects.extra(
                    select={'is_recent':"create_time >'2016-01-01'"},
                    where=['type_no=%s'],
                    params=['12'],
                    order_by=['create_time']
                    ),
                [self.material]
                )

    def test_defer(self):
#        print Material.objects.defer('price','type_no')
        pass

    def test_only(self):
        print "Test only() method: ", Material.objects.only('name','price')

    def test_using(self):
        # 指定查询所使用的数据库，当我们使用多个数据库时使用。
        pass

    def test_select_for_update(self):
        pass

    def test_raw(self):
        print "==========Test raw\n"
        for i in Material.objects.raw('select id, name from material'):
            print i,"\n"
#        self.assertSequenceEqual(Material.objects.raw('select id, name from material').all(),[self.material, self.material2])

    def test_get(self):
        self.assertEqual(Material.objects.get(type_no='24'), self.material2)
        
    def test_get_or_create(self):
        (new_obj, created)=Material.objects.get_or_create(name='Fibra', type_no='24')
        self.assertFalse(created)
        (new_obj,created)=Material.objects.get_or_create(name='Swither', type_no='3',
                defaults={'price':0} 
                )
        self.assertTrue(created)

    def test_update_or_create(self):
        (new_obj, created)=Material.objects.update_or_create(
                                name='Fibra',
                                type_no='24',
                                defaults={ 'type_no':'25' }
                            )
        self.assertFalse(created)

        (new_obj, created)=Material.objects.update_or_create(
                                name='Fibra',
                                type_no='26',
                                defaults={ 
                                    'type_no':'27',
                                    'price':0
                                    }
                            )
        self.assertTrue(created)

    def test_bulk_create(self):
        Material.objects.bulk_create([
                Material.new_('Shoe','35'), 
                Material.new_('Shoe','36'), 
                Material.new_('Shoe','37') 
                ])
        self.assertEqual(Material.objects.filter(name='Shoe').count(), 3)


    def test_first(self):
        self.assertEqual(Material.objects.first(),self.material)

    def test_last(self):
        self.assertEqual(Material.objects.last(), self.material2)

    def test_count(self):
        self.assertEqual(Material.objects.count(), 2)

    # latest/earliest : 依赖于model的Meta类的 get_latest_by 选项值指定的字段
    def test_latest(self):
        self.assertEqual(Material.objects.latest(),self.material2)

    def test_earliest(self):
        self.assertEqual(Material.objects.earliest(), self.material)
        
    def test_delete(self):
        self.material.delete()
        self.assertSequenceEqual(Material.objects.all(), [self.material2])

    def test_exists(self):
        self.assertTrue(Material.objects.filter(type_no='24').exists())
        self.assertFalse(Material.objects.filter(type_no='25').exists())
        
    def test_update(self):
        # update return the number of records it updated
        self.assertEqual(Material.objects.filter(type_no='24').update(type_no='25'),1)
        self.assertEqual(Material.objects.get(type_no='25'), self.material2)

    def test_in_bulk(self):
        self.assertDictEqual(Material.objects.in_bulk([1]),{1:self.material})
        self.assertDictEqual(Material.objects.in_bulk(),{1:self.material, 2:self.material2})

    def test_iterator(self):
        self.assertSequenceEqual(list(Material.objects.iterator()),[self.material, self.material2])

        
    def test_annotate(self):
        # annotate: 为查询出来的结果集中的每个记录添加一个额外的 select 字段，以便之后可以使用。
        from django.db.models.functions import Upper
        objs = Material.objects.filter(type_no='24').annotate(name_upper=Upper('name'))
        self.assertEqual(objs[0].name_upper, objs[0].name.upper())
        
    def test_aggregate(self):
        from django.db.models import Count, Avg, Max, Min, StdDev, Sum, Variance
        agg_user=User(username='agg_test', email='agg_test@mail.com', password='agg_test_password')
        agg_user.save()

        in_material3=InMaterial.new_(agg_user,self.material, count=2)
        in_material3.save()

        out_material3=OutMaterial.new_(agg_user, self.material)
        out_material3.save()

        self.assertEqual(Material.objects.filter(type_no='12').aggregate(Count('ins')),{'ins__count':2})
        self.assertEqual(InMaterial.objects.filter(material__type_no='12').aggregate(Avg('count')),{'count__avg':1.0})
        self.assertEqual(InMaterial.objects.filter(material__type_no='12').aggregate(Max('count')), {'count__max':2})
        self.assertEqual(InMaterial.objects.filter(material__type_no='12').aggregate(Min('count')), {'count__min':0})

        self.assertEqual(InMaterial.objects.filter(material__type_no='12').aggregate(Sum('count')),{'count__sum':2})
        # StdDev/Variance 在 Sqlite中不支持。
#        print InMaterial.objects.filter(material__type_no='12').aggregate(StdDev('count'))
#        print InMaterial.objects.filter(material__type_no='12').aggregate(Variance('count'))
#        print Material.objects.aggregate(Count('ins'))
         

