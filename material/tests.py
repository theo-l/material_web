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





        




