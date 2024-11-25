from django.db import models
from django.conf import settings

class Artist(models.Model):
    """
    Модель исполнителя
    name - имя исполнителя
    biography - краткая биография исполнителя
    """
    name = models.CharField(max_length=60, name='name', unique=True, db_index=True)
    biography = models.TextField(name='biography',blank=True)


class Album(models.Model):
    """
    Модель альбома
    title - название альбома
    artist - связь с исполнителем
    description - описание альбома
    picture - изображение обложки альбома
    """
    title = models.CharField(max_length=60, name="title",db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', name='artist')
    description = models.CharField(max_length=1024, name='description')
    picture = models.ImageField(upload_to='album_covers/',name='picture')

class Genre(models.Model):
    """
    Модель жанра
    name - название жанра
    """
    name = models.CharField(max_length=60,name="name",db_index=True,unique=True)


class Song(models.Model):
    """
    Модель трека
    name - название трека
    artist - связь с исполнителем
    album - связь с альбомом
    genre - жанр трека
    text - текст трека
    description - описание трека
    picture - изображение обложки трека
    """

    name = models.CharField(max_length=60, name='name',db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs', name='artist')
    album = models.ManyToManyField(Album, related_name='songs', name='album',blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='songs', name='genre')
    text = models.CharField(max_length=1024, name='text', blank=True)
    description = models.CharField(max_length=1024, name='description',blank=True)
    picture = models.ImageField(upload_to='song_covers/', name='picture')

class Playlist(models.Model):
    """
    Модель плейлиста
    title - название плейлиста
    user - связь с пользователем
    song - связь с треками
    picture - изображение обложки плейлиста
    """
    title = models.CharField(max_length=60, name='title',db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists', name='user')
    song = models.ManyToManyField(Song, related_name='playlists', name='song')
    picture = models.ImageField(upload_to='playlist_covers/', name='picture')

# Create your models here.
