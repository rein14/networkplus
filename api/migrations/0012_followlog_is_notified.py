# Generated by Django 2.0.4 on 2018-06-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180624_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='followlog',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]
