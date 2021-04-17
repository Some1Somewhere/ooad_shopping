from django.test import TestCase
from .models import Product, Order, CartItem


class UseCase1Test(TestCase):
    def setUp(self):
        Product.objects.create(id=1, name="TShirt", price=1000, slug="item1", description="Testing",)
        Product.objects.create(id=2, name="Shorts", price=1500, slug="item2", description="Testing",recommended= Product.objects.get(name="TShirt"))
        Product.objects.create(id=3, name="Notebook", price=400, slug="item3", description="Testing",)
        Product.objects.create(id=4, name="Pen", price=50, slug="item4", description="Testing", recommended =  Product.objects.get(name="Notebook"))
        Product.objects.get(name ="TShirt").recommended = Product.objects.get(name="Shorts")
        Product.objects.get(name ="Notebook").recommended = Product.objects.get(name="Pen")

        

    def test_UT01(self):
        '''Testing if the product added and the title of the product matches'''
        item = Product.objects.first() 
        
        self.assertTrue(isinstance(item, Product))
        self.assertEqual(item.__str__(), item.name)
        