# Generated by Django 5.0.6 on 2024-10-13 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0005_scene_world'),
    ]

    operations = [
        migrations.AddField(
            model_name='world',
            name='world_cover',
            field=models.ImageField(blank=True, null=True, upload_to='world_cover_images/'),
        ),
    ]