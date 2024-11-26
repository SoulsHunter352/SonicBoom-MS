from django.db import models


class Artist(models.Model):
    """
    Модель исполнителя
    name - имя исполнителя
    biography - краткая биография исполнителя
    """
    name = models.CharField(max_length=60, name='Имя исполнителя', unique=True, db_index=True)
    biography = models.TextField(name='Биография исполнителя',blank=True)


class Album(models.Model):
    """
    Модель альбома
    title - название альбома
    artist - связь с исполнителем
    description - описание альбома
    picture - изображение обложки альбома
    """
    title = models.CharField(max_length=60, name="Название альбома",db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', name='Исполнитель')
    description = models.CharField(max_length=1024, name='Описание альбома')
    picture = models.ImageField(upload_to='/',name='Обложка альбома')

class Genre(models.Model):
    """
    Модель жанра
    name - название жанра
    """
    name = models.CharField(max_length=60, name="Название жанра",db_index=True,unique=True)


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

    name = models.CharField(max_length=60, name='Название трека',db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs', name='Исполнитель')
    album = models.ManyToManyField(Album, related_name='songs', name='Альбомы',blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='songs', name='Исполнитель')
    text = models.CharField(max_length=1024, name='Текст трека', blank=True)
    description = models.CharField(max_length=1024, name='Описание трека',blank=True)
    picture = models.ImageField(upload_to='song_covers/', name='Обложка трека')

class Playlist(models.Model):
    """
    Модель плейлиста
    title - название плейлиста
    user - связь с пользователем
    song - связь с треками
    picture - изображение обложки плейлиста
    """
    title = models.CharField(max_length=60, name='Название плейлиста',db_index=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='playlists', name='Пользователь')
    song = models.ManyToManyField(Song, related_name='playlists', name='Треки')
    picture = models.ImageField(upload_to='', name='Обложка плейлиста')

# Create your models here.
