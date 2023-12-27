# Generated by Django 4.2 on 2023-12-27 17:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_shows', '0006_alter_movieshow_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemahall',
            name='seats',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)]),
        ),
    ]
