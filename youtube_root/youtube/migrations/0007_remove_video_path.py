# Generated by Django 2.2.4 on 2019-08-29 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0006_auto_20190828_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='path',
        ),
    ]