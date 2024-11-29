# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class GenreViewSet(viewsets.ViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def list(self, request):
        genres = self.queryset.all()
        serializer = self.serializer_class(genres, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            genre = serializer.save()
            return Response(self.serializer_class(genre).data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            serializer = self.serializer_class(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist:
            return Response('НИХУЯ Не найдено')

    def update(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            serializer = self.serializer_class(genre, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Genre.DoesNotExist:
            return Response('НИХУЯ Не найдено')

    def delete(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            genre.delete()
            return Response()
        except Genre.DoesNotExist:
            return Response('НИХУЯ НЕ найдено')


class SongViewSet(viewsets.ViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def list(self, request):
        tracks = self.queryset.all()
        serializer = self.serializer_class(tracks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            song = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            serializer = self.serializer_class(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response('НИ-ХУ-Я НЕ НАЙДЕНО')

    def update(self, request, pk=None):
        try:
            track = Song.objects.get(pk=pk)
            serializer = self.serializer_class(track, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Song.DoesNotExist:
            return Response("НИ-ХУ-Я НЕ НАЙДЕНО")

    def partial_update(self, request, pk=None):
        """
        Частично изменяет данные трека.
        """
        try:
            song = Song.objects.get(pk=pk)
            serializer = self.serializer_class(song, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Song.DoesNotExist:
            return Response("SONG НИХУЯ НЕ EXISTS")

    def delete(self, request, pk=None):
        """
        Удаляет трек.
        """
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response()
        except Song.DoesNotExist:
            return Response("SONG НИХУЯ НЕ EXISTS")

    def albums(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            albums = song.album.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response(".!. тебе а не альбомы")


class AlbumViewSet(viewsets.ViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def list(self, request):
        albums = self.queryset.all()
        serializer = self.serializer_class(albums, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            album = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album)
            return Response(serializer.data)
        except Album.DoesNotExist:
            return Response("АЛЬБОМА НИ БУДИИИИИИИИИИТ")

    def update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Album.DoesNotExist:
            return Response("ОБНОВЛЕНИЯ НИ БУДИИИИИИИИИИИТ")

    def partial_update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Album.DoesNotExist:
            return Response('ТАКОГО ОБНОЛВЕНИЯ ТОЖЕ НИ БУДИИИИИТ')

    def delete(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Album.DoesNotExist:
            return Response("ХУЙ ТЕБЕ А НЕ УДАЛЕНИЕ")

    def songs(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            songs = album.songs.all()
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)
        except Album.DoesNotExist:
            return Response("ПЕСЕНОК НЕТ")


class ArtistViewSet(viewsets.ViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

    def list(self, request):
        artists = self.queryset.all()
        serializer = self.serializer_class(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("ХУЙ ТЕБЕ А НЕ АРТИСТ")

    def update(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Artist.DoesNotExist:
            return Response("ПУШКИН ЗАСТРЕЛИЛСЯ")

    def partial_update(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Artist.DoesNotExist:
            return Response("ПУШКИН ЗАСТРЕЛИЛСЯ V2")

    def delete(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            artist.delete()
            return Response()
        except Artist.DoesNotExist:
            return Response("НЕЧЕГО УДАЛЯТЬ, ДЕБИЛ")

    def tracks(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            tracks = artist.song.all()
            serializer = SongSerializer(tracks, many=True)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("NOT_FOUND")

    def albums(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            albums = artist.albums.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("NOT_FOUND")


class PlaylistViewSet(viewsets.ViewSet):
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

    def list(self, request):
        playlists = self.queryset.all()
        serializer = self.serializer_class(playlists, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND")

    def update(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND")

    def partial_update(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND")

    def delete(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            playlist.delete()
            return Response()
        except Playlist.DoesNotExist:
            return Response("NOT EXI")

    def tracks(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            tracks = playlist.song.all()
            serializer = SongSerializer(tracks, many=True)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response("not found")
