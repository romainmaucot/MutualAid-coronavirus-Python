# Generated by Django 3.0.3 on 2020-04-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, max_length=256, null=True, unique=True, verbose_name='Slug'),
        ),
    ]
