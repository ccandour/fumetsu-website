# Generated by Django 5.0.6 on 2024-07-21 11:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fumetsu', '0021_remove_anime_list_title'),
        ('users', '0002_auto_20200416_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff_credits',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=100)),
                ('series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fumetsu.anime_list')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
