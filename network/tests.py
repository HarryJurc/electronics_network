from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import NetworkLink


class NetworkLinkAPITests(APITestCase):
    """
    Тесты для API эндпоинта NetworkLink.
    """

    def setUp(self):
        """
        Настройка тестового окружения.
        Создаем пользователей и несколько объектов для тестирования.
        """
        # Пользователь-сотрудник (с доступом)
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword123',
            is_staff=True,
            is_active=True
        )

        # Обычный пользователь (без доступа)
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpassword123'
        )

        # Тестовые данные
        self.link1 = NetworkLink.objects.create(
            name="Test Factory",
            level=0,
            email="factory@test.com",
            country="Russia",
            city="Moscow"
        )
        self.link2 = NetworkLink.objects.create(
            name="Test Shop",
            level=1,
            email="shop@test.com",
            country="USA",
            city="New York",
            supplier=self.link1
        )

    def test_unauthenticated_access_denied(self):
        """
        Проверяем, что неавторизованный пользователь не может получить доступ к API.
        """
        response = self.client.get('/api/network-links/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_access_denied(self):
        """
        Проверяем, что обычный пользователь (не is_staff) не может получить доступ.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/network-links/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_list_links(self):
        """
        Проверяем, что сотрудник может получить список звеньев сети.
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/api/network-links/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе есть оба наших объекта
        self.assertEqual(len(response.data), 2)

    def test_country_filter(self):
        """
        Проверяем работу фильтрации по стране.
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/api/network-links/?country=Russia')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Factory')

    def test_debt_field_is_readonly(self):
        """
        Проверяем, что поле 'debt' нельзя обновить через API.
        """
        self.client.force_authenticate(user=self.staff_user)

        # Начальное значение задолженности
        initial_debt = self.link2.debt

        # Пытаемся обновить задолженность
        update_data = {'name': 'Updated Shop Name', 'debt': 10000.00}
        response = self.client.patch(f'/api/network-links/{self.link2.id}/', update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем объект из базы данных
        self.link2.refresh_from_db()

        # Проверяем, что имя изменилось, а задолженность - нет
        self.assertEqual(self.link2.name, 'Updated Shop Name')
        self.assertEqual(self.link2.debt, initial_debt)
