# Generated by Django 5.0.6 on 2024-07-21 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0019_remove_anime_list_website_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime_list',
            name='image',
        ),
        migrations.RemoveField(
            model_name='anime_list',
            name='image_bg',
        ),
    ]