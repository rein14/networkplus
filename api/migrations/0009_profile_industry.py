# Generated by Django 2.0.4 on 2018-06-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180503_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='industry',
            field=models.CharField(default='', max_length=100),
        ),
    ]
