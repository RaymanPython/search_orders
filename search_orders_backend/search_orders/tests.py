
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from search_orders.models import Profile, Order


class SearchOrdersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, category='Test Category')
        self.order1 = Order.objects.create(title='Order 1', description='This is the first order', category='Test Category')
        self.order2 = Order.objects.create(title='Order 2', description='This is the second order', category='Another Category')
        self.client = APIClient()

    def test_get_profile(self):
        url = reverse('get-profile', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['category'], self.profile.category)

    def test_create_profile(self):
        url = reverse('create-profile')
        data = {'category': 'New Category'}
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['category'], data['category'])
        
    def test_create_order(self):
        url = reverse('create-order')
        data = {'title': 'New Order', 'description': 'This is a new order', 'category': 'Test Category'}
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['category'], data['category'])
        
    def test_get_relevant_orders(self):
        url = reverse('get-relevant-orders')
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['category'], 'Test Category')
        self.assertEqual(response.data[1]['category'], 'Another Category')
