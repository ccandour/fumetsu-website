# Generated by Django 5.0.6 on 2024-07-04 10:51
import time

from django.db import migrations, models
from httpx import HTTPStatusError

from utils.anilist import get_series_by_name


def add_data(apps, schema_editor):
    Anime_list = apps.get_model('fumetsu', 'Anime_list')
    list = Anime_list.objects.all()
    for series in list:
        try:
            series_anilist = get_series_by_name(series.title)
        except HTTPStatusError:
            print(f'Could not find a matching series for {series.title}')
            continue
        series.name_english = series_anilist.title.english
        series.name_romaji = series_anilist.title.romaji
        series.format = series_anilist.format
        series.status = series_anilist.status
        series.episode_count = series_anilist.episodes
        series.anilist_id = series_anilist.id
        series.save()
        print(f'Updated {series.title}')
        time.sleep(1)


class Migration(migrations.Migration):
    dependencies = [
        ('fumetsu', '0011_delete_key_map'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='anime_list',
        #     name='episode_count',
        #     field=models.IntegerField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='anime_list',
        #     name='format',
        #     field=models.CharField(blank=True, max_length=100, null=True),
        # ),
        # migrations.AddField(
        #     model_name='anime_list',
        #     name='name_english',
        #     field=models.CharField(blank=True, max_length=100, null=True),
        # ),
        # migrations.AddField(
        #     model_name='anime_list',
        #     name='name_romaji',
        #     field=models.CharField(blank=True, max_length=100, null=True),
        # ),
        # migrations.AddField(
        #     model_name='anime_list',
        #     name='status',
        #     field=models.CharField(blank=True, max_length=100, null=True),
        # ),
        migrations.AddField(
            model_name='anime_list',
            name='anilist_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RunPython(add_data),
    ]
