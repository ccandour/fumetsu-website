# Generated by Django 2.2.6 on 2019-12-28 00:12
import time

from django.db import migrations, models

from anime.models import Tags_map, Tags
from fumetsu.models import Anime_list

from utils.anilist import get_series_by_id

tags_to_create = []

def clear_tags_table(apps, schema_editor):
    Tags.objects.all().delete()
    Tags_map.objects.all().delete()

def import_tags_from_anilist(apps, schema_editor):
    db_anime = Anime_list.objects.all()
    for series in db_anime:
        time.sleep(1)
        anilist_series = get_series_by_id(series.anilist_id)
        for tag in anilist_series.genres:
            tag_instance = Tags(
                anime_anilist_id=series.anilist_id,
                label=tag
            )
            tags_to_create.append(tag_instance)


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_alter_anime_url_key_map_alter_odc_name_key_map_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_tags_table),
        migrations.DeleteModel('Tags_map'),
        migrations.RemoveField(
            model_name='tags',
            name='tags_map',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='key_map',
        ),
        migrations.AddField(
            model_name='tags',
            name='anime_anilist_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='tags',
            name='label',
            field=models.CharField(max_length=100),
        ),
        migrations.RunPython(import_tags_from_anilist),
        migrations.RunPython(
            lambda apps, schema_editor: Tags.objects.bulk_create(tags_to_create)
        )
    ]