# Generated by Django 5.0.7 on 2024-09-01 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0023_alter_info_bd_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime_list',
            old_name='subtitles',
            new_name='napisy',
        ),
    ]