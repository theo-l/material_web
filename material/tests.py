import datetime
from django.test import TestCase

from material.models import *
# Create your tests here.
class ModelTest(TestCase):

    def test_material_create(self):
        material=Material.new_('Fibra','12')
        material.save()
        self.assertSequenceEqual(Material.objects.all(),[material])

    def test_material_change(self):
        self.test_material_create()
        material=Material.objects.all()[0]
        material.name="Metal"
        material.save()
        self.assertEqual(Material.objects.)

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

    def test_in_material_creation(self):
        user=User(username='test', email='test@mail.com', password='testpassword')
        material=Material.new_('Fibra','13')
        user.save()
        material.save()
        in_material = InMaterial.new_(user, material)
        in_material.save()
        self.assertEqual(InMaterial.objects.all()[0], in_material)

    def test_in_material_desc_ordering(self):
        
        pass




