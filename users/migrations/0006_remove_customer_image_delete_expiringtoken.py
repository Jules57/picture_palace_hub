# Generated by Django 4.2 on 2023-12-22 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_expiringtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='image',
        ),
        migrations.DeleteModel(
            name='ExpiringToken',
        ),
    ]
