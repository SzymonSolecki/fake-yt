# Generated by Django 2.2.4 on 2019-08-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0002_auto_20190826_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
