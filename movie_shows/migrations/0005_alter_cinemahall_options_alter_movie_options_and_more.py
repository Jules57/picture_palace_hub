# Generated by Django 4.2 on 2023-12-22 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_shows', '0004_alter_order_seat_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cinemahall',
            options={'ordering': ['seats', 'name']},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['title', 'duration_in_minutes']},
        ),
        migrations.AlterModelOptions(
            name='movieshow',
            options={'ordering': ['start_date', 'start_time']},
        ),
    ]
