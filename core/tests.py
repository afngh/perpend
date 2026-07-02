from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import MainTopic, Todo

User = get_user_model()

class AuthAPITests(APITestCase):
    def setUp(self):
        self.login_url = reverse('auth_login')
        self.me_url = reverse('auth_me')
        self.topics_url = reverse('topic_list')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }

    def test_user_login(self):
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
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_topics_auto_seeds_and_returns_data(self):
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Before calling API, DB should be empty
        self.assertEqual(MainTopic.objects.filter(user=user).count(), 0)

        response = self.client.get(self.topics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # After calling API, DB should have loaded the roadmaps from json directory
        self.assertGreater(MainTopic.objects.filter(user=user).count(), 0)
        self.assertGreater(Todo.objects.filter(main_topic__user=user).count(), 0)

        # Inspect fields in returned list
        self.assertIn('domain', response.data[0])
        self.assertIn('todos', response.data[0])

    def test_todo_retrieve_and_update(self):
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Trigger seeding
        self.client.get(self.topics_url)

        todo = Todo.objects.filter(main_topic__user=user).first()
        self.assertIsNotNone(todo)
        
        todo_detail_url = reverse('todo_detail', kwargs={'pk': todo.pk})
        
        # Get Todo details
        response = self.client.get(todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subtopic_id'], todo.subtopic_id)
        
        # Update Todo details
        update_data = {
            'completed': True,
            'notes': 'Completed my study notes on DSA constraints.',
            'github_url': 'https://github.com/afngh/perpend/blob/main/core/models.py'
        }
        response = self.client.patch(todo_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed'], True)
        self.assertEqual(response.data['status'], 'completed')
        self.assertEqual(response.data['notes'], update_data['notes'])
        self.assertEqual(response.data['github_url'], update_data['github_url'])

        # Verify DB values were updated and persisted
        todo.refresh_from_db()
        self.assertTrue(todo.completed)
        self.assertEqual(todo.status, 'completed')
        self.assertEqual(todo.notes, update_data['notes'])
        self.assertEqual(todo.github_url, update_data['github_url'])

