# Generated by Django 5.0.1 on 2025-01-21 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_formsubmission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formsubmission',
            name='read_at',
        ),
    ]
