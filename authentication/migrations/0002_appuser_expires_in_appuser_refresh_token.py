# Generated by Django 5.1.5 on 2025-04-01 03:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='expires_in',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='appuser',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
