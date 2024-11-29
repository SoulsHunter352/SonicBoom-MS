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
    print(old_image.name, new_image.name)
    if old_image and old_image.name != ARTIST_DEFAULT and old_image.name != new_image.name:
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
    print(old_image.name, new_image.name)
    if old_image and old_image.name != ALBUM_DEFAULT and old_image.name != new_image.name:
        old_image.delete(save=False)
