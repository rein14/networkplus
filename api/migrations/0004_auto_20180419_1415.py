# Generated by Django 2.0.4 on 2018-04-19 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180418_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='full_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default='', max_length=150),
        ),
    ]