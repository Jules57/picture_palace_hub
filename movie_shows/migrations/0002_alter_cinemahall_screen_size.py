# Generated by Django 4.2 on 2023-12-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_shows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemahall',
            name='screen_size',
            field=models.CharField(choices=[('Standard', 'Standard'), ('Large', 'Large'), ('Premium', 'Premium')], default='Standard', max_length=50),
        ),
    ]