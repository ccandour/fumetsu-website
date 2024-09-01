from django.db import migrations, models, transaction
import time
from anime.models import Tag
from fumetsu.models import AnimeSeries
from utils.anilist import get_series_by_id
from utils.utils import tag_label_to_polish

tags_to_create = []

def clear_and_import_tags(apps, schema_editor):
    with transaction.atomic():
        db_anime = AnimeSeries.objects.all()
        for series in db_anime:
            print(f'Getting tags for {series.name_english}')
            time.sleep(1)
            anilist_series = get_series_by_id(series.anilist_id)
            for tag in anilist_series.genres:
                tag_instance = Tag(
                    anime_anilist_id=series.anilist_id,
                    label=tag,
                    label_polish=tag_label_to_polish(tag)
                )
                tags_to_create.append(tag_instance)
        Tag.objects.bulk_create(tags_to_create)

class Migration(migrations.Migration):
    dependencies = [
        ('anime', '0006_alter_anime_url_key_map_alter_odc_name_key_map_and_more'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='tags',
            name='label_polish',
            field=models.CharField(max_length=100),
        ),
        migrations.RunPython(clear_and_import_tags),
    ]