# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .mixins import CustomPermissionMixin
from .models import *
from .serializers import *
# from users.permissions import IsModerator


class GenreViewSet(CustomPermissionMixin,viewsets.ViewSet):
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            serializer = self.serializer_class(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist:
            return Response('Ничего Не найдено', status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            serializer = self.serializer_class(genre, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Genre.DoesNotExist:
            return Response('Ничего Не найдено',status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            genre = self.queryset.get(pk=pk)
            genre.delete()
            return Response()
        except Genre.DoesNotExist:
            return Response('Ничего НЕ найдено',status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = self.serializer_class(genre, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Genre.DoesNotExist:
            return Response("Genre Ничего НЕ EXISTS", status=status.HTTP_404_NOT_FOUND)

class SongViewSet(CustomPermissionMixin,viewsets.ViewSet):
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
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            serializer = self.serializer_class(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response('Ничего НЕ НАЙДЕНО',status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            track = Song.objects.get(pk=pk)
            serializer = self.serializer_class(track, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            return Response("Ничего НЕ НАЙДЕНО",status=status.HTTP_404_NOT_FOUND)

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
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            return Response("SONG Ничего НЕ EXISTS",status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        """
        Удаляет трек.
        """
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response()
        except Song.DoesNotExist:
            return Response("SONG Ничего НЕ EXISTS",status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        try:
            song = Song.objects.get(pk=pk)
            albums = song.album.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response("Нет альбомов",status=status.HTTP_404_NOT_FOUND)


class AlbumViewSet(CustomPermissionMixin, viewsets.ViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def list(self, request):
        albums = self.queryset.all()
        serializer = self.serializer_class(albums, many=True)
        return Response(serializer.data)

    # @permission_classes(IsModerator)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            album = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album)
            return Response(serializer.data)
        except Album.DoesNotExist:
            return Response("АЛЬБОМА НИ БУДИИИИИИИИИИТ", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response("ОБНОВЛЕНИЯ НИ БУДИИИИИИИИИИИТ", status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            serializer = self.serializer_class(album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response('ТАКОГО ОБНОЛВЕНИЯ ТОЖЕ НИ БУДИИИИИТ', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            album.delete()
            return Response()
        except Album.DoesNotExist:
            return Response("не получилось удалить", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        try:
            album = Album.objects.get(pk=pk)
            songs = album.songs.all()
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)
        except Album.DoesNotExist:
            return Response("ПЕСЕНОК НЕТ", status=status.HTTP_404_NOT_FOUND)


class ArtistViewSet(CustomPermissionMixin, viewsets.ViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        artists = self.queryset.all()
        serializer = self.serializer_class(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("артиста нет", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Artist.DoesNotExist:
            return Response("артиста нет", status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = self.serializer_class(artist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Artist.DoesNotExist:
            return Response("артиста нет V2", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            artist.delete()
            return Response()
        except Artist.DoesNotExist:
            return Response("НЕЧЕГО УДАЛЯТЬ", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def tracks(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            tracks = artist.songs.all()
            serializer = SongSerializer(tracks, many=True)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("NOT_FOUND", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        try:
            artist = Artist.objects.get(pk=pk)
            albums = artist.albums.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response("NOT_FOUND", status=status.HTTP_404_NOT_FOUND)


class PlaylistViewSet(CustomPermissionMixin,viewsets.ViewSet):
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
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND",status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND",status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = self.serializer_class(playlist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Playlist.DoesNotExist:
            return Response("NOT FOUND",status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            playlist.delete()
            return Response()
        except Playlist.DoesNotExist:
            return Response("NOT EXI",status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def tracks(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            tracks = playlist.song.all()
            serializer = SongSerializer(tracks, many=True)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response("not found",status=status.HTTP_404_NOT_FOUND)
