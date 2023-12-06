# Generated by Django 2.2.9 on 2020-02-17 19:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KH_Key_map',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id_anime', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('web_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='KH_Odc_name',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ep_nr', models.IntegerField(blank=True, null=True)),
                ('ep_title', models.FloatField()),
                ('title', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('napisy', models.FileField(blank=True, upload_to='kh_napisy/')),
                ('key_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hentaiterment.KH_Key_map')),
            ],
        ),
        migrations.CreateModel(
            name='KH_Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('image', models.ImageField(default='anime_default.jpg', upload_to='kh_anime_post')),
                ('odc_nm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hentaiterment.KH_Odc_name')),
            ],
        ),
        migrations.CreateModel(
            name='KH_Anime_url',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('web_site', models.CharField(max_length=100)),
                ('ep_nr', models.IntegerField()),
                ('link', models.TextField()),
                ('odc_nm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hentaiterment.KH_Odc_name')),
            ],
        ),
        migrations.CreateModel(
            name='KH_Anime_list',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('image', models.ImageField(default='av_default.gif', upload_to='kh_anime_avatar')),
                ('image_bg', models.ImageField(default='anime_bg.jpg', upload_to='kh_anime_avatar')),
                ('key_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hentaiterment.KH_Key_map')),
            ],
        ),
    ]
