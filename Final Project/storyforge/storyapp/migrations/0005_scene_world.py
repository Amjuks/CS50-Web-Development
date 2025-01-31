# Generated by Django 5.0.6 on 2024-10-13 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0004_remove_world_locations_alter_character_world_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scene',
            name='world',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='scenes', to='storyapp.world'),
            preserve_default=False,
        ),
    ]
