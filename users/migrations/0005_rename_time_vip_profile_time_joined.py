# Generated by Django 5.0.7 on 2024-09-01 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_ban_remove_profile_nap_vip_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='time_vip',
            new_name='time_joined',
        ),
    ]
