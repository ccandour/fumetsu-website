# Generated by Django 5.0.6 on 2024-07-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0005_anime_list_napisy'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime_list',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='anime_list',
            name='web_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
