# Generated by Django 5.1.1 on 2024-11-25 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_rename_биография_исполнителя_artist_biography_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='cover',
            new_name='picture',
        ),
    ]