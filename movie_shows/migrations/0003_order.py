# Generated by Django 4.2 on 2023-12-11 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_shows', '0002_alter_cinemahall_screen_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_quantity', models.PositiveIntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ordered_at', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('movie_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='movie_shows.movieshow')),
            ],
        ),
    ]
