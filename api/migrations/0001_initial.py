# Generated by Django 2.0.4 on 2018-04-16 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.TextField(default='')),
                ('username', models.TextField(default='')),
                ('profile_privacy', models.CharField(default='public', max_length=100, verbose_name='public/follower')),
                ('security_code', models.CharField(default='', max_length=255)),
                ('isVarified', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
