# Generated by Django 2.0.4 on 2018-05-03 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_notificationsprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsprofile',
            name='notification_type',
            field=models.CharField(max_length=100),
        ),
    ]