from django.db import migrations

def copy_key_map_data(apps, schema_editor):
    Anime_list = apps.get_model('fumetsu', 'Anime_list')
    for anime in Anime_list.objects.all():
        anime.title = anime.key_map.title
        anime.web_name = anime.key_map.web_name
        anime.save()

class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0006_anime_list_title_anime_list_web_name'),  # replace with the previous migration name
    ]

    operations = [
        migrations.RunPython(copy_key_map_data),
    ]
