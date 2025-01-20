from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

User = get_user_model()


class AuthTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        User.objects.create_user(
            username="test_user",
            email="test@test.com",
            password="test_password"
        )

        self.login_endpoint = reverse('token-obtain-pair')
        self.refresh_endpoint = reverse('token-refresh')
    
    def test_login(self):
        """
        Test login endpoint, should return a valid access and refresh token
        """
        payload = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(path=self.login_endpoint, data=payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_wrong_password(self):
        """
        Test login endpoint with wrong password, should return 401
        """
        payload = {
            'username': 'test_user',
            'password': 'wrong_password'
        }
        response = self.client.post(path=self.login_endpoint, data=payload, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')


    def test_login_wrong_username(self):
        payload = {
            'username': 'wrong_user',
            'password': 'test_password'
        }
        response = self.client.post(path=self.login_endpoint, data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')


    def test_refresh_token(self):
        payload = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(path=self.login_endpoint, data=payload, format='json')
        refresh_token = response.data['refresh']

        payload = {
            'refresh': refresh_token
        }
        response = self.client.post(path=self.refresh_endpoint, data=payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertNotEqual(refresh_token, response.data['access'])
