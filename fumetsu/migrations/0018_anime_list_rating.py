# Generated by Django 5.0.6 on 2024-07-19 18:51
import time

from django.db import migrations, models

from fumetsu.models import AnimeSeries
from utils.anilist import get_series_by_id

def add_rating(apps, schema_editor):
    db_series = AnimeSeries.objects.all()
    for series in db_series:
        time.sleep(2)  # Be mindful of rate limiting
        anilist_id = series.anilist_id
        if anilist_id:
            series_data = get_series_by_id(anilist_id)
            print(f'Updating {series_data.title.english}')
            series.rating = series_data.average_score
            series.save()



class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0017_alter_relation_id'),
    ]

    operations = [
        migrations.RunPython(add_rating)
    ]
