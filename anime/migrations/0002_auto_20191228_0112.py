# Generated by Django 2.2.6 on 2019-12-28 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='key_map',
        ),
        migrations.AddField(
            model_name='odc_name',
            name='ep_title',
            field=models.TextField(default='0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='odc_name',
            name='ep_nr',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
