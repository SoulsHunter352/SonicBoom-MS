from io import BytesIO
from tkinter import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from PIL import Image

from .mixins import ViewSetTestsMixin
from .models import Artist, Album, Genre, Song,Playlist
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer, GenreSerializer,PlaylistSerializer


def create_image():
    image_data = BytesIO()
    Image.new('RGB', (100, 100)).save(image_data, 'PNG')
    image_data.seek(0)
    return image_data


class SongSerializerTests(APITestCase):
    def setUp(self):
        # Создание предварительных данных
        self.artist = Artist.objects.create(name='Artist A', biography='Famous artist')
        self.album1 = Album.objects.create(title='Album 1', artist=self.artist)
        self.album2 = Album.objects.create(title='Album 2', artist=self.artist)
        self.genre = Genre.objects.create(name='Rock')
        self.music_content = b'music'
        self.music_file = SimpleUploadedFile('test.mp3', self.music_content, content_type='audio/mpeg')
    def test_create_valid(self):
        data = {
            'name': 'Song A',
            'artist': self.artist.id,
            'album': [self.album1.id],
            'genre': self.genre.id,
            'text': 'Lyrics of song A',
            'description': 'A great song.',
            'track': self.music_file
        }
        serializer = SongSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        #self.assertEqual(serializer.is_valid(), True)
        song = serializer.save()
        song.album.set(data['album'])

        self.assertEqual(song.name, 'Song A')
        self.assertEqual(song.artist, self.artist)
        self.assertEqual(list(song.album.all()), [self.album1])
        self.assertEqual(song.genre, self.genre)
        self.assertTrue(song.track, '/media/defaults/song_track_default.png')

    def test_create_invalid(self):
        data = {
            'name': None,
            'artist': None,
            'album': [],
            'genre': None,
            'track': self.music_file,
            'text': 'Lyrics of song A',
            'description': 'A great song.',
        }
        serializer = SongSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

    def test_update_valid(self):
        song = Song.objects.create(
            name='Song A',
            artist=self.artist,
            genre=self.genre,
            track=self.music_file,
            text='Lyrics of song A',
            description='A great song.',
        )
        song.album.set([self.album1])

        data = {
            'name': 'Song B',
            'artist': self.artist.id,
            'album': [self.album2.id],
            'genre': self.genre.id,
            'track': self.music_file,
            'text': 'Updated lyrics for song B',
            'description': 'An updated great song.'
        }

        serializer = SongSerializer(instance=song, data=data)
        self.assertEqual(serializer.is_valid(), True)
        updated_song = serializer.save()
        updated_song.album.set(data['album'])

        self.assertEqual(updated_song.name, 'Song B')
        self.assertEqual(updated_song.artist, self.artist)
        self.assertEqual(list(updated_song.album.all()), [self.album2])
        self.assertEqual(updated_song.genre, self.genre)
        self.assertTrue(updated_song.track, '/media/defaults/song_track_default.png')

    def test_update_invalid(self):
        song = Song.objects.create(
            name='Song A',
            artist=self.artist,
            genre=self.genre,
            track=self.music_file,
            text='Lyrics of song A',
            description='A great song.',
            picture='path/to/image.jpg',
        )
        song.album.set([self.album1])

        data = {
            'name': None,
            'artist': None,
            'album': [],
            'genre': None,
            'track': self.music_file,
        }

        serializer = SongSerializer(instance=song, data=data)
        self.assertEqual(serializer.is_valid(), False)


class GenreSerializerTests(APITestCase):

    def setUp(self):
        # Создание предварительных данных
        self.genre = Genre.objects.create(name='Rock')

    def test_create_valid_genre(self):
        data = {
            'name': 'Pop'
        }
        serializer = GenreSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        genre = serializer.save()

        self.assertEqual(genre.name, 'Pop')
        self.assertTrue(Genre.objects.filter(name='Pop').exists())

    def test_create_invalid_genre(self):
        data = {
            'name': ''
        }
        serializer = GenreSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_update_valid_genre(self):
        data = {
            'name': 'Jazz'
        }
        serializer = GenreSerializer(instance=self.genre, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_genre = serializer.save()

        self.assertEqual(updated_genre.name, 'Jazz')
        self.assertTrue(Genre.objects.filter(name='Jazz').exists())
        self.assertFalse(Genre.objects.filter(name='Rock').exists())

    def test_update_invalid_genre(self):
        data = {
            'name': ''
        }
        serializer = GenreSerializer(instance=self.genre, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class PlaylistSerializerTests(APITestCase):
    def setUp(self):
        # Создание предварительных данных
        User = get_user_model()
        self.music_content = b'music'
        self.test_genre1 = Genre.objects.create(name='Pop')
        self.test_genre2 = Genre.objects.create(name='Rock')
        self.artist1 = Artist.objects.create(name='Иван', biography='')
        self.music_file = SimpleUploadedFile('test.mp3', self.music_content, content_type='audio/mpeg')
        self.user = User.objects.create_user(username='testuser', password='password', login='User1', email='User1@gmail.com')
        self.song1 = Song.objects.create(name='Test Song 1', artist=self.artist1, genre=self.test_genre1 ,track=self.music_file)
        self.song2 = Song.objects.create(name='Test Song 2', artist=self.artist1, genre=self.test_genre2,track=self.music_file)
        self.playlist = Playlist.objects.create(title='Test Playlist', user=self.user)
        self.playlist.song.set([self.song1])

    def test_create_valid_playlist(self):
        data = {
            'title': 'New Playlist',
            'user': self.user.id,
            'song': [self.song1.id, self.song2.id],
        }
        serializer = PlaylistSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        playlist = serializer.save()

        self.assertEqual(playlist.title, 'New Playlist')
        self.assertEqual(playlist.user, self.user)
        self.assertEqual(list(playlist.song.all()), [self.song1, self.song2])
        self.assertTrue(Playlist.objects.filter(title='New Playlist').exists())

    def test_create_invalid_playlist(self):
        data = {
            'title': '',
            'user': self.user.id,
            'song': []
        }
        serializer = PlaylistSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    def test_update_valid_playlist(self):
        data = {
            'title': 'Updated Playlist',
            'user': self.user.id,
            'song': [self.song2.id],
        }
        serializer = PlaylistSerializer(instance=self.playlist, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_playlist = serializer.save()

        self.assertEqual(updated_playlist.title, 'Updated Playlist')
        self.assertEqual(updated_playlist.user, self.user)
        self.assertEqual(list(updated_playlist.song.all()), [self.song2])

    def test_update_invalid_playlist(self):

        data = {
            'title': '',
            'user': self.user.id,
            'song': None,
            'picture': None
        }
        serializer = PlaylistSerializer(instance=self.playlist, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


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


class ArtistViewSetTests(ViewSetTestsMixin, APITestCase):
    model = Artist
    list_url = reverse('artist-list')
    detail_url = reverse('artist-detail', kwargs={'pk': 1})
    wrong_url = reverse('artist-detail', kwargs={'pk': 999})

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        image_data = BytesIO()
        Image.new('RGB', (100, 100)).save(image_data, 'PNG')
        image_data.seek(0)

        # cls.image = SimpleUploadedFile('album.jpg', image_data.getvalue())
        data = {'name': 'New Artist', 'biography': ''}
        cls.artist = Artist.objects.create(**data)

        album_image = SimpleUploadedFile('album.jpg', image_data.getvalue())
        Album.objects.create(title='Album 1', artist=cls.artist, description='Альбом', picture=album_image)
        album_image = SimpleUploadedFile('album2.jpg', image_data.getvalue())
        Album.objects.create(title='Album 2', artist=cls.artist, description='Альбом', picture=album_image)

        genre = Genre.objects.create(name='Рок')

        music_content = b'music'
        music_file = SimpleUploadedFile('test.mp3', music_content, content_type='audio/mpeg')
        Song.objects.create(name='Track 1', artist=cls.artist, genre=genre, track=music_file)
        music_file = SimpleUploadedFile('test.mp3', music_content, content_type='audio/mpeg')
        Song.objects.create(name='Track 2', artist=cls.artist, genre=genre, track=music_file)

        cls.create_data = {
            'name': 'New Artist2',
            'picture': SimpleUploadedFile('album2.jpg', image_data.getvalue()),
            'biography': ''
        }

        cls.create_valid = cls.create_data.copy()
        cls.create_valid['id'] = 2
        cls.create_valid['picture'] = '/media/artist_covers/album2.jpg'

        cls.retrieve_data = data.copy()
        cls.retrieve_data['id'] = 1
        cls.retrieve_data['picture'] = '/media/defaults/artist_default.png'

        cls.partial_data = {'name': 'Updated Artist'}
        cls.partial_valid_data = cls.retrieve_data.copy()
        cls.partial_valid_data['name'] = 'Updated Artist'

        cls.update_data = cls.create_data.copy()
        cls.update_valid = cls.create_data.copy()
        cls.update_valid['id'] = 1
        cls.update_valid['picture'] = '/media/artist_covers/album2.jpg'

    def test_create_valid(self):
        super().test_create_valid()
        self.model.objects.get(pk=self.create_valid['id']).picture.delete()

    def test_update_valid(self):
        super().test_update_valid()
        self.model.objects.get(pk=self.update_valid['id']).picture.delete()

    def test_albums_valid(self):
        response = self.client.get(reverse('artist-albums', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_albums_invalid(self):
        response = self.client.get(self.wrong_url + '/albums/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tracks_valid(self):
        response = self.client.get(reverse('artist-tracks', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tracks_invalid(self):
        response = self.client.get(self.wrong_url + '/tracks/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AlbumViewSetTests(ViewSetTestsMixin, APITestCase):
    model = Album
    list_url = reverse('album-list')
    detail_url = reverse('album-detail', kwargs={'pk': 1})
    wrong_url = reverse('album-detail', kwargs={'pk': 999})

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image = create_image()

        cls.artist = Artist.objects.create(name='New Artist', biography='')

        Album.objects.create(**{
            'title': 'New Album',
            'artist': cls.artist,
            'description': 'Album',
            'picture': SimpleUploadedFile('album1.jpg', cls.image.getvalue())
        })

        cls.create_data = {
            'title': 'New Album2',
            'artist': cls.artist.pk,
            'description': 'Album',
            'picture': SimpleUploadedFile('album2.jpg', cls.image.getvalue())
        }
        cls.create_valid = {
            'id': 2,
            'title': 'New Album2',
            'artist': cls.artist.pk,
            'description': 'Album',
            'picture': '/media/album_covers/album2.jpg'
        }

        cls.retrieve_data = {
            'id': 1,
            'title': 'New Album',
            'artist': cls.artist.pk,
            'description': 'Album',
            'picture': '/media/album_covers/album1.jpg'
        }

        cls.partial_data = {
            'title': 'Album'
        }
        cls.partial_valid_data = cls.retrieve_data.copy()
        cls.partial_valid_data['title'] = 'Album'
        cls.update_data = cls.create_data.copy()
        cls.update_valid = cls.create_data.copy()
        cls.update_valid['id'] = 1
        cls.update_valid['picture'] = '/media/album_covers/album2.jpg'

        genre = Genre.objects.create(name='Рок')
        music_content = b'music'
        music_file = SimpleUploadedFile('test.mp3', music_content, content_type='audio/mpeg')
        Song.objects.create(name='Track 1', artist=cls.artist, genre=genre, track=music_file)

    def test_create_valid(self):
        super().test_create_valid()
        self.model.objects.get(pk=self.create_valid['id']).picture.delete()

    def test_update_valid(self):
        super().test_update_valid()
        self.model.objects.get(pk=self.update_valid['id']).picture.delete()

    def test_songs_valid(self):
        response = self.client.get(reverse('album-songs', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_songs_invalid(self):
        response = self.client.get(reverse('album-songs', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GenreViewSetTests(ViewSetTestsMixin, APITestCase):
    model = Genre
    list_url = reverse('genre-list')
    detail_url = reverse('genre-detail', kwargs={'pk': 1})
    wrong_url = reverse('genre-detail', kwargs={'pk': 999})

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Genre.objects.create(**{
            'name': 'New Genre'
        })

        cls.create_data = {
            'name': 'New Genre1'
        }
        cls.create_valid = {
            'id': 2,
            'name': 'New Genre1'
        }

        cls.retrieve_data = {
            'id': 1,
            'name': 'New Genre'
        }

        cls.partial_data = {
            'name': 'ROCK'
        }
        cls.partial_valid_data = cls.retrieve_data.copy()
        cls.partial_valid_data['name'] = 'ROCK'
        cls.update_data = cls.create_data.copy()
        cls.update_valid = cls.create_data.copy()
        cls.update_valid['id'] = 1
    def test_create_invalid2(self):
        data = {}
        response = self.client.post(self.list_url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SongViewSetTests(ViewSetTestsMixin,APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image = create_image()
        # Инициализация данных для тестов
        cls.model = Song
        cls.list_url = reverse('song-list')
        cls.detail_url = reverse('song-detail', kwargs={'pk': 1})
        cls.wrong_url = reverse('song-detail', kwargs={'pk': 999})

        # Создание тестовых объектов
        cls.artist = Artist.objects.create(name='New Artist32143', biography='')
        cls.genre = Genre.objects.create(name='Cuntry324432')
        cls.album =         Album.objects.create(**{
            'title': 'New Album1',
            'artist': cls.artist,
            'description': 'Album',
            'picture': SimpleUploadedFile('album1.jpg', cls.image.getvalue())
        })
        cls.album2 =         Album.objects.create(**{
            'title': 'New Album2',
            'artist': cls.artist,
            'description': 'Album',
            'picture': SimpleUploadedFile('album1.jpg', cls.image.getvalue())
        })
        cls.song = Song.objects.create(name='New Song',artist=cls.artist,genre=cls.genre)
        cls.song.album.set([cls.album,cls.album2])
        # Подготовка данных для создания песни
        music_content = b'music'
        cls.music_file = SimpleUploadedFile('test.mp3', music_content, content_type='audio/mpeg')
        cls.create_data = {
            'name': 'New Song',
            'artist': cls.artist.pk,
            'genre': cls.genre.pk,
            'album':[cls.album.pk,cls.album2.pk]
        }
        cls.create_valid = cls.create_data.copy()
        cls.create_valid['id'] = 2
        cls.create_valid['picture'] = '/media/defaults/song_default.png'
        cls.create_valid['track'] = '/media/defaults/song_track_default.mp3'
        cls.create_valid['text'] = ''
        cls.create_valid['description'] = ''


        cls.retrieve_data = cls.create_valid.copy()
        cls.retrieve_data['id'] = 1

        cls.partial_data = {'name':'new super test track'}
        cls.partial_valid_data = cls.retrieve_data.copy()
        cls.partial_valid_data['name'] = 'new super test track'

        cls.update_data = cls.create_data.copy()
        cls.update_data['name'] = "New song name"
        cls.update_data['id'] = 1
        cls.update_valid = cls.retrieve_data.copy()
        cls.update_valid['name'] = "New song name"
    def test_albums_valid(self):
        response = self.client.get(reverse('song-albums', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_albums_invalid(self):
        response = self.client.get(reverse('song-albums', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PlaylistViewSetTests(ViewSetTestsMixin,APITestCase):
    @classmethod
    def setUpTestData(cls):

        super().setUpTestData()
        # Инициализация данных для тестов
        cls.model = Playlist
        cls.list_url = reverse('playlist-list')
        cls.detail_url = reverse('playlist-detail', kwargs={'pk': 1})
        cls.wrong_url = reverse('playlist-detail', kwargs={'pk': 999})
        test_User = get_user_model()
        cls.artist = Artist.objects.create(name='New Artist3214343', biography='')
        cls.genre = Genre.objects.create(name='Cuntry32443432')
        cls.test_user = test_User.objects.create_user(username='tester32', password='password', login='User2',email='User2@gmail.com')
        cls.playlist = Playlist.objects.create(title='Test Playlist',user=cls.test_user)
        music_content = b'music'
        cls.music_file = SimpleUploadedFile('test.mp3', music_content, content_type='audio/mpeg')
        cls.song1 = Song.objects.create(name='New Song1', artist=cls.artist, genre=cls.genre)
        cls.song2 = Song.objects.create(name='New Song2', artist=cls.artist, genre=cls.genre)
        cls.playlist.song.set([cls.song1, cls.song2])
        # Подготовка данных для создания песни


        cls.create_data = {
            'title': 'Test Playlist',
            'user': cls.test_user.pk,
            'song': [cls.song1.pk,cls.song2.pk]
        }
        cls.create_valid = cls.create_data.copy()
        cls.create_valid['id'] = 2
        cls.create_valid['picture'] = '/media/defaults/playlist_default.png'

        cls.retrieve_data = cls.create_valid.copy()
        cls.retrieve_data['id'] = 1

        cls.partial_data = {'title': 'new super test album'}
        cls.partial_valid_data = cls.retrieve_data.copy()
        cls.partial_valid_data['title'] = 'new super test album'

        cls.update_data = cls.create_data.copy()
        cls.update_data['title'] = "New playlist name"
        cls.update_data['id'] = 1
        cls.update_valid = cls.retrieve_data.copy()
        cls.update_valid['title'] = "New playlist name"

    def test_songs_valid(self):
        response = self.client.get(reverse('playlist-tracks', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_songs_invalid(self):
        response = self.client.get(reverse('playlist-tracks', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
