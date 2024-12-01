from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomPermissionMixin:
    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


class ViewSetTestsMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(login='test', email='test@gmail.com', username='user',
                                                        password='12345699uq', role=get_user_model().ADMIN)

    def setUp(self):
        self.client.login(username=self.user.login, password='12345699uq')

    def test_list_valid(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_guest(self):
        self.client.logout()
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_valid(self):
        # data = {'name': 'New Artist2', 'picture': self.image, 'biography': ''}
        response = self.client.post(self.list_url, data=self.create_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.create_valid)
        self.model.objects.get(pk=self.create_valid['id']).picture.delete()

    def test_create_invalid(self):
        data = {}
        response = self.client.post(self.list_url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
