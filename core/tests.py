from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAPITests(APITestCase):
    def setUp(self):
        self.login_url = reverse('auth_login')
        self.me_url = reverse('auth_me')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }


    def test_user_login(self):
        """
        Verify that a registered user can log in and retrieve tokens + user metadata.
        """
        # First register
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_user_me_authenticated(self):
        """
        Verify that an authenticated user can fetch their profile.
        """
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        # Register and get access token
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        access_token = response.data['access']
        
        # Apply bearer authorization token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_me_unauthenticated(self):
        """
        Verify that access to the profile endpoint is denied without credentials.
        """
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
