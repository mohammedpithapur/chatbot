# Generated by Django 5.0.1 on 2024-02-02 05:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
