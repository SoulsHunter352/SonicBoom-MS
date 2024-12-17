from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.models import User
from users.serializers import UserSerializer, RegisterUserSerializer, LoginSerializer, ChangePasswordSerializer


class UserSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            login="test_user",
            email="old@example.com",
            username="Old Name"
        )

    def test_update_positive(self):
        """
        Тест Б1: Метод update UserSerializer (положительный).
        """
        data = {"email": "new@example.com", "username": "New Name"}
        serializer = UserSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.email, "new@example.com")
        self.assertEqual(updated_user.username, "New Name")

    def test_update_negative(self):
        """
        Тест Б2: Метод update UserSerializer (отрицательный).
        """
        data = {"email": None, "username": None}
        serializer = UserSerializer(instance=self.user, data=data, partial=True)

        self.assertFalse(serializer.is_valid())

        # Теперь проверяем, что при попытке сохранить возникает ValidationError
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)  # это сразу вызовет ошибку, если данные невалидны
            serializer.save()

class RegisterUserSerializerTest(APITestCase):
    def test_create_positive(self):
        """
        Тест Б3: Метод create RegisterUserSerializer (положительный).
        """
        data = {
            "login": "new_user",
            "email": "user@example.com",
            "username": "User Name",
            "password1": "Pass1234",
            "password2": "Pass1234",
            "role": User.COMMON
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.login, "new_user")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.username, "User Name")

    def test_create_negative(self):
        """
        Тест Б4: Метод create RegisterUserSerializer (отрицательный).
        """
        data = {
            "login": "new_user",
            "email": "user@example.com",
            "username": "User Name",
            "password1": "Pass1234",
            "password2": "DifferentPass",
            "role": User.COMMON
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password2", serializer.errors)

    def test_validate_positive(self):
        """
        Тест Б5: Метод validate RegisterUserSerializer (положительный).
        """
        data = {"password1": "Pass1234", "password2": "Pass1234"}
        serializer = RegisterUserSerializer()
        validated_data = serializer.validate(data)
        self.assertEqual(validated_data["password1"], "Pass1234")

    def test_validate_negative(self):
        """
        Тест Б6: Метод validate RegisterUserSerializer (отрицательный).
        """
        data = {"password1": "Pass1234", "password2": "DifferentPass"}
        serializer = RegisterUserSerializer()
        with self.assertRaises(ValidationError):
            serializer.validate(data)


class LoginSerializerTest(APITestCase):
    def setUp(self):
        """
        Создаем тестового пользователя с кастомной моделью.
        """
        self.user = User.objects.create_user(
            login='test_user',                  # Уникальный логин
            email='test_user@example.com',      # Почта
            username='Test Username',          # Имя пользователя (если требуется)
            password='Pass1234'                # Пароль
        )

    def test_validate_positive(self):
        """
        Тест Б7: Метод validate LoginSerializer (положительный).
        """
        data = {'login': 'test_user', 'password': 'Pass1234'}
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            print("Errors:", serializer.errors)

        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        self.assertEqual(validated_data['login'], 'test_user')
        self.assertEqual(validated_data['password'], 'Pass1234')

        self.assertEqual(serializer.get_user(), self.user)

    def test_validate_negative(self):
        """
        Тест Б8: Метод validate LoginSerializer (отрицательный).
        """
        data = {'login': None, 'password': None}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ChangePasswordSerializerTest(APITestCase):
    def setUp(self):
        """
        Настраиваем пользователя для теста.
        """
        self.user = User.objects.create_user(
            login='test_user',
            email='test_user@example.com',
            username='Test User',
            password='OldPass123'  # Хешируем пароль
        )
    def test_validate_positive(self):
        """
        Тест Б9: Метод validate ChangePasswordSerializer (положительный).
        """
        data = {
            'old_password': 'OldPass123',
            'new_password1': 'NewPass123',
            'new_password2': 'NewPass123'
        }

        serializer = ChangePasswordSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        self.assertEqual(validated_data['new_password1'], 'NewPass123')
        self.assertEqual(validated_data['new_password2'], 'NewPass123')

    def test_validate_negative(self):
        """
        Тест Б10: Метод validate ChangePasswordSerializer (отрицательный).
        """
        data = {
            'old_password': 'OldPass123',
            'new_password1': 'NewPass123',
            'new_password2': 'DifferentPass'
        }

        serializer = ChangePasswordSerializer(instance=self.user, data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("new_password2", context.exception.detail)

    def test_update_positive(self):
        """
        Тест Б11: Метод update ChangePasswordSerializer (положительный).
        """
        data = {
            'old_password': 'OldPass123',
            'new_password1': 'NewPass123',
            'new_password2': 'NewPass123'
        }

        # Передаем пользователя в instance
        serializer = ChangePasswordSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        # Выполняем обновление пароля
        user = serializer.save()

        # Проверяем, что новый пароль установлен
        self.assertTrue(check_password('NewPass123', user.password))

    def test_update_negative(self):
        """
        Тест Б12: Метод update ChangePasswordSerializer (отрицательный).
        """
        # Создаем пользователя с паролем
        user = User.objects.create_user(
            login='213test_user',
            username='test_user',
            email='12test_user@example.com',
            password='OldPass123'
        )

        data = {
            'old_password': 'WrongOldPass123',
            'new_password1': 'NewPass123',
            'new_password2': 'NewPass123'
        }

        serializer = ChangePasswordSerializer(data=data, instance=user)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class UserViewSetTests(APITestCase):
    def setUp(self):
        # Создаем пользователей для теста
        self.user1 = get_user_model().objects.create_user(
            login='user1',
            email='user1@example.com',
            username='User One',
            password='Pass1234'
        )
        self.user2 = get_user_model().objects.create_user(
            login='user2',
            email='user2@example.com',
            username='User Two',
            password='Pass1234'
        )

        self.user = User.objects.create_user(
            login="testuser",
            username="Test User",
            email="test@example.com",
            password="Password123!",
            role="common"
        )
        self.update_url = f"/api/users/{self.user2.id}/"
        self.retrieve_url = self.update_url
        self.delete_url = self.retrieve_url


    def test_list_users(self):
        """
        Тест Б13: Проверка возвращаемого списка всех пользователей.
        """
        # Выполняем запрос к API
        response = self.client.get('/api/users/')  # Путь к UserViewSet (например, /api/users/)

        # Проверяем статус ответа и корректность списка
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ожидаем 2 пользователя
        self.assertEqual(response.data[0]['login'], self.user1.login)
        self.assertEqual(response.data[1]['login'], self.user2.login)

    def test_list_users_invalid_serializer(self):
        """
        Тест Б14: Некорректный сериализатор (ошибка в serializer_class).
        """
        with self.assertRaises(AttributeError):
            response = self.client.get('/api/users/')
            response.raise_for_status()

    def test_create_user(self):
        """
        Тест Б15: Создание нового пользователя.
        """
        data = {
            'login': 'new43143user',
            'email': 'user@example.com',
            'username': 'userk5445',
            'password1': 'Pass1234',
            'password2': 'Pass1234',
            'role': 'common'
        }
        response = self.client.post('/api/users/', data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['user']['login'], data['login'])
        self.assertEqual(response.data['user']['email'], data['email'])
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['role'], data['role'])

    def test_create_user_invalid(self):
        """
        Тест Б16: Создание пользователя с некорректными данными.
        """
        data = {
            'login': None,
            'email': None,
            'username': None,
            'password1': 'Pass1234',
            'password2': 'Pass1234',
            'role': 'common'
        }

        response = self.client.post('/api/users/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('login', response.data)  # Проверка, что ошибка валидации для поля login
        self.assertIn('email', response.data)  # Проверка, что ошибка валидации для поля email

    def test_update_user(self):
        """
        Тест Б17: Полное обновление данных пользователя (положительный).
        """
        data = {
            'login': 'new43413411431user',
            'email': 'user413413411@example.com',
            'username': 'userk34ac54451',
            'password1': 'Pass1234',
            'password2': 'Pass1234',
            'role': 'common'
        }
        response = self.client.put(self.update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])

    def test_update_user_invalid(self):
        """
        Тест Б18: Полное обновление с некорректными данными (отрицательный).
        """
        data = {'username': None}
        response = self.client.put(self.update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_partial_update_user(self):
        """
        Тест Б19: Частичное обновление данных пользователя (положительный).
        """
        data = {'username': 'Partially Updated Name'}
        response = self.client.patch(self.update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])

    def test_partial_update_user_invalid(self):
        """
        Тест Б20: Частичное обновление с некорректными данными (отрицательный).
        """
        data = {'username': None}
        response = self.client.patch(self.update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_retrieve_user(self):
        """
        Тест Б21: Получение данных пользователя (положительный).
        """
        response = self.client.get(self.retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    def test_retrieve_user_not_found(self):
        """
        Тест Б22: Получение данных несуществующего пользователя (отрицательный).
        """
        invalid_url = "/users/999/"  # ID несуществующего пользователя
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_delete_user(self):
        """
        Тест Б23: Удаление пользователя (положительный).
        """
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            get_object_or_404(User, id=self.user.id)

    def test_delete_user_not_found(self):
        """
        Тест Б24: Удаление несуществующего пользователя (отрицательный).
        """
        invalid_url = "/api/users/999/"  # ID несуществующего пользователя
        response = self.client.delete(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No User matches the given query.')