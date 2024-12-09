# Generated by Django 5.1.1 on 2024-12-01 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_remove_answer_текст_ответа_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='status',
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.CharField(choices=[('open', 'OPEN'), ('closed', 'CLOSED')], default='open', max_length=6),
        ),
    ]
