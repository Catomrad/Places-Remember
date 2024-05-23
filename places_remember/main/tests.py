from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Memory


# Create your tests here.


class MemoryCreationTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.create_memory_url = reverse('add_memory')

    def test_create_memory(self):
        # Данные для нового воспоминания
        memory_data = {
            'title': 'Test Memory',
            'description': 'This is a test memory.',
            'latitude': 55.7558,
            'longitude': 37.6173
        }

        response = self.client.post(self.create_memory_url, data=memory_data)

        # Проверяем, что редирект произошел успешно
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))

        # Проверяем, что воспоминание создано в базе данных
        self.assertEqual(Memory.objects.count(), 1)
        memory = Memory.objects.first()
        self.assertEqual(memory.title, memory_data['title'])
        self.assertEqual(memory.description, memory_data['description'])
        self.assertEqual(memory.latitude, memory_data['latitude'])
        self.assertEqual(memory.longitude, memory_data['longitude'])
        self.assertEqual(memory.user, self.user)


class MemoryListTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.profile_url = reverse('profile')

        # Создаем несколько воспоминаний для тестового пользователя
        Memory.objects.create(user=self.user, title='Memory 1', description='Description 1', latitude=55.7558,
                              longitude=37.6173)
        Memory.objects.create(user=self.user, title='Memory 2', description='Description 2', latitude=48.8566,
                              longitude=2.3522)

    def test_memory_list(self):
        response = self.client.get(self.profile_url)

        # Проверяем, что запрос выполнен успешно
        self.assertEqual(response.status_code, 200)

        # Проверяем, что воспоминания передаются в контексте
        self.assertIn('memories', response.context)

        # Проверяем, что количество воспоминаний в контексте соответствует количеству в базе данных
        memories = response.context['memories']
        self.assertEqual(len(memories), 2)

        # Проверяем данные первых воспоминаний
        self.assertEqual(memories[0].title, 'Memory 1')
        self.assertEqual(memories[0].description, 'Description 1')
        self.assertEqual(memories[0].latitude, 55.7558)
        self.assertEqual(memories[0].longitude, 37.6173)

        self.assertEqual(memories[1].title, 'Memory 2')
        self.assertEqual(memories[1].description, 'Description 2')
        self.assertEqual(memories[1].latitude, 48.8566)
        self.assertEqual(memories[1].longitude, 2.3522)