# Generated by Django 5.0.7 on 2024-09-01 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0011_rename_subtitles_odc_name_napisy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='odc_name',
            old_name='napisy',
            new_name='subtitles',
        ),
    ]
