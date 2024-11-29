from django.dispatch import receiver
from django.db import models

from .models import Artist, Album

ARTIST_DEFAULT = 'defaults/artist_default.png'
ALBUM_DEFAULT = ''


@receiver(models.signals.pre_delete, sender=Artist)
def delete_artist_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        if instance.picture.name != ARTIST_DEFAULT:
            instance.picture.delete()


@receiver(models.signals.pre_delete, sender=Album)
def delete_album_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.picture:
        if instance.picture.name != ALBUM_DEFAULT:
            instance.picture.delete()
