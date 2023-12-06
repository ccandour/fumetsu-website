# Generated by Django 2.2.1 on 2019-11-03 20:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fumetsu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odc_name',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ep_nr', models.IntegerField()),
                ('title', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('napisy', models.FileField(blank=True, upload_to='napisy/')),
                ('key_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fumetsu.Key_map')),
            ],
        ),
        migrations.CreateModel(
            name='Tags_map',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fumetsu.Key_map')),
                ('tags_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.Tags_map')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('image', models.ImageField(default='anime_default.jpg', upload_to='anime_post')),
                ('key_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fumetsu.Key_map')),
                ('odc_nm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.Odc_name')),
            ],
        ),
        migrations.CreateModel(
            name='Anime_url',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('web_site', models.CharField(max_length=100)),
                ('ep_nr', models.IntegerField()),
                ('link', models.TextField()),
                ('key_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fumetsu.Key_map')),
                ('odc_nm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.Odc_name')),
            ],
        ),
    ]
