import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
import uuid
from django.http import HttpRequest
from django.urls import reverse
from .models import Memory, User
from .views import add_memory, profile


class MemoryCreationTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(vk_id=str(uuid.uuid4()), first_name='Test', last_name='User')

    def test_create_memory(self):
        # Данные для нового воспоминания
        memory_data = {
            'title': 'Test Memory',
            'description': 'This is a test memory.',
            'latitude': 55.7558,
            'longitude': 37.6173
        }

        # Создаем фиктивный запрос с данными формы
        request = HttpRequest()
        request.method = 'POST'
        request.POST = memory_data
        request.session = {'user_id': self.user.id}

        # Вызываем представление напрямую
        response = add_memory(request)

        # Проверяем, что редирект произошел успешно
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('profile'))

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
        self.user = User.objects.create(vk_id=str(uuid.uuid4()), first_name='Test', last_name='User')
        self.client = Client()

        # Аутентифицируем пользователя, добавляя user_id в сессию
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Создаем несколько воспоминаний для тестового пользователя
        Memory.objects.create(user=self.user, title='Memory 1', description='Description 1', latitude=55.7558, longitude=37.6173)
        Memory.objects.create(user=self.user, title='Memory 2', description='Description 2', latitude=48.8566, longitude=2.3522)

    def test_memory_list(self):
        response = self.client.get(reverse('profile'))

        # Проверяем, что запрос выполнен успешно
        self.assertEqual(response.status_code, 200)

        # Извлекаем контекст из ответа
        context = response.context

        # Проверяем, что воспоминания передаются в контексте
        self.assertIn('memories', context)

        # Проверяем, что количество воспоминаний в контексте соответствует количеству в базе данных
        memories = context['memories']
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


if __name__ == '__main__':
    unittest.main()
