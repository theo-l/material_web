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


    #Test Q object queries
    def test_Q_object_queries(self):
        self.test_in_material_create()
        




