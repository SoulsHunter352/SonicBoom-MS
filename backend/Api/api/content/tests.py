from io import BytesIO
from tkinter import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase

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
