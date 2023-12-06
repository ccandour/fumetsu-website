# Generated by Django 2.2.6 on 2020-04-04 18:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0004_episode_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player_valid',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ilosc', models.IntegerField(default=1)),
                ('key_map_ep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.Odc_name')),
            ],
        ),
    ]
