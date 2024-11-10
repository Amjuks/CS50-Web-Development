# Generated by Django 5.0.6 on 2024-10-06 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0003_character_world_location_world_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='world',
            name='locations',
        ),
        migrations.AlterField(
            model_name='character',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyapp.world'),
        ),
        migrations.AlterField(
            model_name='location',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='storyapp.world'),
        ),
    ]