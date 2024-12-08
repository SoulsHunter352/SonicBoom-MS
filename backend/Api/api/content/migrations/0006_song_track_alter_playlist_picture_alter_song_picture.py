# Generated by Django 5.1.1 on 2024-11-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_rename_исполнитель_album_artist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='track',
            field=models.FileField(default='', upload_to='songs/'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='picture',
            field=models.ImageField(blank=True, upload_to='playlist_covers/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='picture',
            field=models.ImageField(blank=True, upload_to='song_covers/'),
        ),
    ]
