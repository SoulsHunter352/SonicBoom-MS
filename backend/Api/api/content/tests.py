from io import BytesIO
from tkinter import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from PIL import Image

from .models import Artist, Album
from .serializers import ArtistSerializer, AlbumSerializer


class ArtistSerializerTests(APITestCase):
    def test_create_valid(self):
        serializer = ArtistSerializer(data={'name': 'Artist A', 'biography': 'Famous artist'})
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Artist A', 'biography': 'Famous artist',
                                           'picture': '/media/defaults/artist_default.png'})

    def test_create_invalid(self):
        serializer = ArtistSerializer(data={'name': None, 'biography': None})
        self.assertEqual(serializer.is_valid(), False)

    def test_update_valid(self):
        artist = Artist.objects.create(name='Artist A', biography='Famous artist')
        serializer = ArtistSerializer(instance=artist, data={'name': 'Artist B'})
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Artist B', 'biography': 'Famous artist',
                                           'picture': '/media/defaults/artist_default.png'})

    def test_update_invalid(self):
        artist = Artist.objects.create(name='Artist A', biography='Famous artist')
        serializer = ArtistSerializer(instance=artist, data={'name': None})
        self.assertEqual(serializer.is_valid(), False)


class AlbumSerializerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = Artist.objects.create(name='Artist A', biography='Famous artist')
        image_data = BytesIO()
        Image.new('RGB', (100, 100)).save(image_data, 'PNG')
        image_data.seek(0)
        cls.image = SimpleUploadedFile('album.jpg', image_data.getvalue())

    def test_create_valid(self):
        serializer = AlbumSerializer(data={'title': 'Album A', 'description': 'First album',
                                           'artist': 1, 'picture': self.image})
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.assertEqual(serializer.data, {'id': 1, 'title': 'Album A', 'description': 'First album',
                                           'artist': 1, 'picture': '/media/album_covers/album.jpg'})
        Album.objects.get(pk=1).picture.delete()  # Удаление картинки после теста

    def test_create_invalid(self):
        serializer = AlbumSerializer(data={'title': None, 'description': None,
                                           'artist': None, 'picture': None})
        self.assertEqual(serializer.is_valid(), False)

    def test_update_valid(self):
        album = Album.objects.create(title='Album A', description='First album',
                                     artist=self.artist, picture=self.image)
        serializer = AlbumSerializer(instance=album, data={'title': 'Album B'}, partial=True)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.assertEqual(serializer.data, {'id': 1, 'title': 'Album B', 'description': 'First album',
                                           'artist': 1, 'picture': '/media/album_covers/album.jpg'})
        album.picture.delete()  # Удаление картинки после теста

    def test_update_invalid(self):
        album = Album.objects.create(title='Album A', description='First album',
                                     artist=self.artist, picture=self.image)
        serializer = AlbumSerializer(instance=album, data={'title': None}, partial=True)
        self.assertEqual(serializer.is_valid(), False)
        album.picture.delete()  # Удаление картинки после теста


class ArtistViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(login='test', email='test@gmail.com', username='user',
                                                        password='12345699uq', role=get_user_model().ADMIN)
        cls.list_url = reverse('artist-list')
        cls.detail_url = reverse('artist-detail', kwargs={'pk': 1})

        image_data = BytesIO()
        Image.new('RGB', (100, 100)).save(image_data, 'PNG')
        image_data.seek(0)
        cls.image = SimpleUploadedFile('album.jpg', image_data.getvalue())

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
        data = {'name': 'New Artist', 'picture': self.image}
        response = self.client.post(self.list_url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data['id'] = 1
        data['picture'] = '/media/artist_covers/album.jpg'
        data['biography'] = ''
        self.assertEqual(response.data, data)
        Artist.objects.get(pk=data['id']).picture.delete()

    def test_create_invalid(self):
        data = {}
        response = self.client.post(self.list_url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid(self):
        data = {'name': 'New Artist', 'biography': ''}
        artist = Artist.objects.create(**data)
        response = self.client.put(
            self.detail_url,
            data={'name': 'Updated Artist', 'picture': self.image, 'biography': ''},
            format='multipart'
        )

        data['id'] = 1
        data['name'] = 'Updated Artist'
        data['picture'] = '/media/artist_covers/album.jpg'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
        artist = Artist.objects.get(pk=1)
        artist.picture.delete()

    def test_update_invalid(self):
        response = self.client.put(
            reverse('artist-detail', kwargs={'pk': 999}),
            data={'name': 'Updated Artist', 'picture': self.image, 'biography': ''},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_valid(self):
        data = {'name': 'New Artist', 'biography': ''}
        artist = Artist.objects.create(**data)
        response = self.client.patch(
            self.detail_url,
            data={'name': 'Updated Artist'},
        )
        data['id'] = 1
        data['name'] = 'Updated Artist'
        data['picture'] = '/media/defaults/artist_default.png'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_partial_update_invalid(self):
        response = self.client.put(
            reverse('artist-detail', kwargs={'pk': 999}),
            data={'name': 'Updated Artist'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrive_update_invalid(self):
        response = self.client.get(reverse('artist-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
