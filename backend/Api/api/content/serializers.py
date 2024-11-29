from rest_framework import serializers
from .models import Song,Album,Artist,Playlist,Genre
from django.contrib.auth import get_user_model
from django.conf import settings

class SongSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    album = serializers.PrimaryKeyRelatedField(many=True, queryset=Album.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Song
        fields = [
            'id', 'name', 'artist', 'album', 'genre', 'track', 'text', 'description', 'picture',]

        def create(self, validated_data):
            album = validated_data.pop('album', [])
            song = Song.objects.create(**validated_data)
            song.album.set(album)
            return song

        def update(self, validated_data,instance):
            album = validated_data.pop('album',None)
            instance.name = validated_data.get('name', instance.name)
            instance.artist = validated_data.get('artist', instance.artist)
            instance.genre = validated_data.get('genre', instance.genre)
            instance.track = validated_data.get('track', instance.track)
            instance.text = validated_data.get('text', instance.text)
            instance.description = validated_data.get('description', instance.description)
            instance.picture = validated_data.get('picture', instance.picture)
            instance.save()
            if album is not None:
                instance.album.set(album)
            return instance


class GenreSerializer(serializers.ModelSerializer):
    #name = serializers.CharField()
    class Meta:
        model = Genre
        fields = ['id','name']
    def create(self, validated_data):
        return Genre.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'picture', 'biography']

    def create(self, validated_data):
        return Artist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.save()
        return instance


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'description', 'picture']
    def create(self, validated_data):
        return Album.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.description = validated_data.get('description', instance.description)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Playlist

User = get_user_model()

class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'user', 'song', 'picture']

    def create(self, validated_data):
        songs = validated_data.pop('song', [])
        playlist = Playlist.objects.create(**validated_data)
        playlist.song.set(songs)
        return playlist

    def update(self, instance, validated_data):
        songs = validated_data.pop('song', None)
        instance.title = validated_data.get('title', instance.title)
        instance.user = validated_data.get('user', instance.user)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        if songs is not None:
            instance.song.set(songs)

        return instance

