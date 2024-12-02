from django.test import TestCase
from .serializers import RegisterUserSerializer, LoginSerializer
from .models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from content import mixins

viewSetTests = mixins.ViewSetTestsMixin()

# Create your tests here.
class TestRegisterUserSerializer(TestCase):
    def test_valid_data(self):
        data = {
            "login": "testuser",
            "email": "test@example.com",
            "username": "Test User",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!"
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.login, data["login"])
        self.assertTrue(user.check_password(data["password1"]))

    def test_password_mismatch(self):
        data = {
            "login": "testuser",
            "email": "test@example.com",
            "username": "Test User",
            "password1": "StrongPassword123!",
            "password2": "WeakPassword123!"
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password2", serializer.errors)

class TestLoginSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            login="testuser", email="test@example.com", username="Test User", password="StrongPassword123!"
        )

    def test_valid_login(self):
        data = {"login": "testuser", "password": "StrongPassword123!"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.get_user(), self.user)

    def test_invalid_login(self):
        data = {"login": "wronguser", "password": "StrongPassword123!"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            login="testuser", email="test@example.com", username="Test User", password="StrongPassword123!"
        )
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_user(self):
        data = {
            "login": "newuser",
            "email": "newuser@example.com",
            "username": "New User",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['login'], data["login"])

    def test_retrieve_user(self):
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['login'], self.user.login)

    def test_update_user(self):
        data = {"username": "Updated User"}
        response = self.client.patch(f'/api/users/{self.user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data["username"])

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())