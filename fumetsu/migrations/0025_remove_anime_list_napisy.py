# Generated by Django 5.0.7 on 2024-09-01 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0024_rename_subtitles_anime_list_napisy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime_list',
            name='napisy',
        ),
    ]
