import django
from django.db import migrations, models, transaction


def copy_key_map_to_temp(apps, schema_editor):
    Odc_name = apps.get_model('anime', 'Odc_name')
    Anime_url = apps.get_model('anime', 'Anime_url')
    Tags = apps.get_model('anime', 'Tags')

    models_to_update = [Odc_name, Anime_url, Tags]

    for model in models_to_update:
        for item in model.objects.all():
            if item.key_map:
                item.key_map_temp = item.key_map.web_name
                item.save()
                print(f"Updated {model.__name__} id {item.id} with key_map_temp {item.key_map_temp}")


def transfer_key_map_to_anime_list(apps, schema_editor):
    Anime_list = apps.get_model('fumetsu', 'Anime_list')
    Odc_name = apps.get_model('anime', 'Odc_name')
    Anime_url = apps.get_model('anime', 'Anime_url')
    Tags = apps.get_model('anime', 'Tags')

    models_to_update = [Odc_name, Anime_url, Tags]

    with transaction.atomic():
        for model in models_to_update:
            for item in model.objects.all():
                if item.key_map_temp and item.key_map_temp != "":
                    try:
                        anime = Anime_list.objects.get(web_name=item.key_map_temp)
                        item.key_map = anime
                        item.save()
                        print(f"Linked {model.__name__} id {item.id} to Anime_list id {anime.id}")
                    except Anime_list.DoesNotExist:
                        print(
                            f"No Anime_list found for {model.__name__} id {item.id} with key_map_temp {item.key_map_temp}")
                        item.key_map = None  # Clear the key_map if no corresponding Anime_list entry is found
                        item.save()


def validate_foreign_keys(apps, schema_editor):
    Odc_name = apps.get_model('anime', 'Odc_name')
    Anime_url = apps.get_model('anime', 'Anime_url')
    Tags = apps.get_model('anime', 'Tags')
    Anime_list = apps.get_model('fumetsu', 'Anime_list')

    models_to_check = [Odc_name, Anime_url, Tags]

    for model in models_to_check:
        for item in model.objects.all():
            try:
                if item.key_map:
                    Anime_list.objects.get(id=item.key_map.id)
            except Anime_list.DoesNotExist:
                print(f"Orphaned key_map found in {model.__name__} id {item.id} with key_map id {item.key_map.id}")
                item.key_map = None
                item.save()


class Migration(migrations.Migration):
    dependencies = [
        ('anime', '0005_player_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime_url',
            name='key_map_temp',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='odc_name',
            name='key_map_temp',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='key_map_temp',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.RunPython(copy_key_map_to_temp),
        migrations.AlterField(
            model_name='anime_url',
            name='key_map',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='fumetsu.anime_list'),
        ),
        migrations.AlterField(
            model_name='odc_name',
            name='key_map',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='fumetsu.anime_list'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='key_map',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='fumetsu.anime_list'),
        ),
        migrations.RunPython(transfer_key_map_to_anime_list),
        migrations.RunPython(validate_foreign_keys),
        migrations.RemoveField(
            model_name='tags',
            name='key_map_temp',
        ),
        migrations.RemoveField(
            model_name='anime_url',
            name='key_map_temp',
        ),
        migrations.RemoveField(
            model_name='odc_name',
            name='key_map_temp',
        ),
    ]
