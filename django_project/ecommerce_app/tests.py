from django.test import TestCase
from django.core import exceptions
from .models import Product, Order, CartItem
from . import cart
from django.test import Client
from django.conf import settings
from importlib import import_module

class TestCase1(TestCase):

    def test_UT01(self):
        '''UT01 : Testing if search returns the correct values'''
        response = Client().get('/',{"q":"Test"})
        self.assertQuerysetEqual(response.context['results'],Product.objects.all(), ordered=False)
        
    def test_UT02(self):
        '''UT02: Testing if the individual product page loads successfully'''
        response = Client().get('/product/1/item1/')    
        self.assertEqual(response.status_code, 200)
    

    def test_UT03(self):
        '''UT03 : Testing if empty search returns a valid page'''
        response = Client().get('/',{"q":""})
        self.assertQuerysetEqual(response.context['results'],Product.objects.all(), ordered=False)
        
    
        
    
    def test_UT06(self):
        '''UT06 : Testing if the product gets added to cart and the details matches.'''
        c = Client()
        c.post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        cartItem = CartItem.objects.first()
        self.assertTrue(isinstance(cartItem,CartItem))
        self.assertEqual(cartItem.__str__(), "{}:{}".format(cartItem.product.name, cartItem.id))
        
    def test_UT09(self):
        '''UT09 : Testing if the product gets added to cart and the details matches.'''
        c = Client()
        c.post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        cartItem = CartItem.objects.first()
        self.assertTrue(isinstance(cartItem,CartItem))
        self.assertEqual(cartItem.__str__(), "{}:{}".format(cartItem.product.name, cartItem.id))
        
    
   
        
    
        
class TestCase2(TestCase):
      def setUp(self):
        # http://code.djangoproject.com/ticket/10899
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
    
    
      def test_UT201(self):
        '''UT201: Cart page loads when empty'''
        response = Client().get('/cart/')    
        self.assertEqual(response.status_code, 200)
        
      def test_UT202(self):
        '''UT202: Changing quantity or removing in cart is succesful'''
        
        Client().post('/cart/', {'item_id': '1', 'quantity': '4', 'submit':'Update'})
        response = Client().get('/cart/')    
        self.assertEqual(response.status_code, 200)
        Client().post('/cart/', {'item_id': '1',  'submit':"Remove"})
        response = Client().get('/cart/')    
        self.assertEqual(response.status_code, 200)
        
    
        
      def test_UT203(self):
        '''UT203: Cart page loads when having items'''
        
        Client().post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        response = Client().get('/cart/')    
        self.assertEqual(response.status_code, 200)
    
      def test_UT204(self):
        '''UT204: Changing quantity in is reflected'''
        Client().post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        Client().post('/cart/', {'item_id': '1', 'quantity': '4', 'submit':'Update'})
        cartItem = CartItem.objects.get(id=1)
        self.assertTrue(isinstance(cartItem,CartItem))
        self.assertEqual(cartItem.quantity,4)
        
      def test_UT205(self):
        '''UT205: Remove product  is reflected'''
        Client().post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        Client().post('/cart/', {'item_id': '1', 'submit':'Remove'})
        try:
            CartItem.objects.get(id=1)
        except exceptions.ObjectDoesNotExist:
            pass
        
      def test_UT206(self):
        '''UT206: Non Text  inputs doesn't update UI'''
        Client().post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        Client().post('/cart/', {'item_id': '1', 'quantity': 'abcd', 'submit':'Update'})
        cartItem = CartItem.objects.get(id=1)
        self.assertTrue(isinstance(cartItem,CartItem))
        self.assertEqual(cartItem.quantity,1)
        
      def test_UT207(self):
        '''UT207: Appropriate bill amount being reflected which changes as items are updated'''
        Client().post('/product/1/item1/', {'product_id': '1', 'quantity': '1'})
        Client().post('/cart/', {'item_id': '1', 'quantity': '4', 'submit':'Update'})
        cartItem = CartItem.objects.get(id=1)
        self.assertTrue(isinstance(cartItem,CartItem))
        self.assertEqual(cartItem.quantity,4)
        self.assertEqual(cartItem.price,1000)
           
    
    
    
        
      def test_UT209(self):
        '''UT209: Checking if order gets created successfully'''
        Client().post('/checkout/',{"name":"Dhruv","email":"dhruvshetty3@gmail.com","postal_code":"560094","address":"Testing"})
        order = Order.objects.first()
        self.assertTrue(isinstance(order,Order))
        self.assertEqual(order.__str__(), "{}:{}".format(order.id, order.email))
        
class TestCase3(TestCase):
        
    def test_UT301(self):
        '''UT301: Testing if the results are in the order of clicks'''
        response = Client().get('/')
        electronics = Product.objects.filter(category='Electronics').order_by('-clicks')
        stationary = Product.objects.filter(category='Stationary').order_by('-clicks')
        general = Product.objects.filter(category='General').order_by('-clicks')

        self.assertQuerysetEqual(response.context['electronics'],electronics)
        self.assertQuerysetEqual(response.context['stationary'],stationary)
        self.assertQuerysetEqual(response.context['general'],general)
        
    
    def test_UT302(self):
        '''UT302: Testing if the results in search page are in the order of clicks'''
        response = Client().get('/',{"q":""})
        self.assertQuerysetEqual(response.context['results'],Product.objects.all().order_by('-clicks'))
        
    def test_UT303(self):
        '''UT303 : Search result page should show relevant items to what was searched'''
        response = Client().get('/',{"q":"Test"})
        self.assertQuerysetEqual(response.context['results'],Product.objects.all(), ordered=False)
    
    def test_UT304(self):
        '''UT304: Testing for electronics in electronics'''
        response = Client().get('/product/1/item1/')
        self.assertQuerysetEqual(response.context['similarProducts'],Product.objects.filter(category = "Electronics").exclude(id=1), ordered=False)
        
    def test_UT305(self):
        '''UT305: Testing for stationary in stationary'''
        response = Client().get('/product/3/item3/')
        self.assertQuerysetEqual(response.context['similarProducts'],Product.objects.filter(category = "Stationary").exclude(id=3), ordered=False)
        

    def test_UT306(self):
        '''UT306: Testing for electronics in stationary'''
        response = Client().get('/product/1/item1/')
        result_products = [product.id for product in Product.objects.filter(category = "Electronics")]
        for product in response.context['similarProducts']:
            self.assertFalse(product in result_products)
        
    def test_UT307(self):
        '''UT307: Testing for stationary in electronics'''
        response = Client().get('/product/3/item3/')
        result_products = [product.id for product in Product.objects.filter(category = "Electronics")]
        for product in response.context['similarProducts']:
            self.assertFalse(product in result_products)
            
    def test_UT308(self):
        '''UT308: Seller recommendations should be visible if available on product page'''
        response = Client().get('/product/3/item3/')
        self.assertEqual(response.context['product'],Product.objects.get(id=3))
        
    def test_UT309(self):
        '''UT309: Product page recommendations also ordered by number of clicks'''
        response = Client().get('/product/3/item3/')
        self.assertQuerysetEqual(response.context['similarProducts'],Product.objects.filter(category = "Stationary").exclude(id=3), ordered=False)
        

            
    def test_UT310(self):
        '''UT310: The selected item should not be recommended again on its information page'''
        response = Client().get('/product/1/item1/')
        product = Product.objects.get(id=1)
        result_products = [product.id for product in Product.objects.filter(category = product.category)]
        for product in response.context['similarProducts']:
            self.assertFalse(product in result_products)
        
        
