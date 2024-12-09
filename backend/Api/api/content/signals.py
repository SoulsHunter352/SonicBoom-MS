from django.dispatch import receiver
from django.db import models

from .models import Artist, Album, Song, Playlist

ARTIST_DEFAULT = 'defaults/artist_default.png'
ALBUM_DEFAULT = ''
SONG_TRACK_DEFAULT = 'defaults/song_track_default.mp3'
SONG_PICTURE_DEFAULT = 'defaults/song_default.png'
PLAYLIST_DEFAULT = 'defaults/playlist_default.png'


@receiver(models.signals.pre_delete, sender=Artist)
def delete_artist_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        if instance.picture.name != ARTIST_DEFAULT:
            instance.picture.delete()


@receiver(models.signals.pre_delete, sender=Song)
def delete_song_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        if instance.picture.name != SONG_PICTURE_DEFAULT:
            instance.picture.delete()


@receiver(models.signals.pre_delete, sender=Song)
def delete_song_track(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.track:
        if instance.track.name != SONG_TRACK_DEFAULT:
            instance.track.delete()


@receiver(models.signals.pre_delete, sender=Playlist)
def delete_playlist_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        if instance.picture.name != PLAYLIST_DEFAULT:
            instance.picture.delete()

@receiver(models.signals.pre_delete, sender=Album)
def delete_album_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        # print('Куку')
        if instance.picture.name != ALBUM_DEFAULT:
            instance.picture.delete()


@receiver(models.signals.pre_save, sender=Artist)
def update_artist_picture(sender, **kwargs):
    instance = kwargs.get('instance')

    if not instance or not instance.pk:
        return

    try:
        old_image = Artist.objects.get(pk=instance.pk).picture
    except Artist.DoesNotExist:
        return
    new_image = instance.picture
    # print(old_image.name, new_image.name)
    if old_image and old_image.name != ARTIST_DEFAULT and old_image.name != new_image.name:
        # print('Удалили', old_image.name)
        old_image.delete(save=False)


@receiver(models.signals.pre_save, sender=Album)
def update_album_picture(sender, instance, **kwargs):
    # instance = kwargs.get('instance')

    if not instance or not instance.pk:
        return

    try:
        old_image = Album.objects.get(pk=instance.pk).picture
    except Album.DoesNotExist:
        return
    new_image = instance.picture
    # print(old_image.name, new_image.name)
    if old_image and old_image.name != ALBUM_DEFAULT and old_image.name != new_image.name:
        old_image.delete(save=False)


@receiver(models.signals.pre_save, sender=Song)
def update_song_picture(sender, instance, **kwargs):
    # instance = kwargs.get('instance')

    if not instance or not instance.pk:
        return
    try:
        old_image = Song.objects.get(pk=instance.pk).picture
    except Song.DoesNotExist:
        return
    new_image = instance.picture
    # print(old_image.name, new_image.name)
    if old_image and old_image.name != SONG_PICTURE_DEFAULT and old_image.name != new_image.name:
        old_image.delete(save=False)


@receiver(models.signals.pre_save, sender=Song)
def update_song_track(sender, instance, **kwargs):
    # instance = kwargs.get('instance')

    if not instance or not instance.pk:
        return

    try:
        old_track = Song.objects.get(pk=instance.pk).track
    except Song.DoesNotExist:
        return
    new_track = instance.track
    # print(old_image.name, new_image.name)
    if old_track and old_track.name != SONG_TRACK_DEFAULT and old_track.name != new_track.name:
        old_track.delete(save=False)


@receiver(models.signals.pre_save, sender=Playlist)
def update_playlist_picture(sender, instance, **kwargs):
    # instance = kwargs.get('instance')
    if not instance or not instance.pk:
        return
    try:
        old_image = Playlist.objects.get(pk=instance.pk).picture
    except Playlist.DoesNotExist:
        return
    new_image = instance.picture
    # print(old_image.name, new_image.name)
    if old_image and old_image.name != PLAYLIST_DEFAULT and old_image.name != new_image.name:
        old_image.delete(save=False)