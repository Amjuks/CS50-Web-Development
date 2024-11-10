# Generated by Django 5.0.6 on 2024-10-02 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('backstory', models.TextField(blank=True, null=True)),
                ('traits', models.JSONField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='characters/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('significance', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='locations/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='storyapp.character')),
                ('related_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to', to='storyapp.character')),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('plot', models.TextField(blank=True, null=True)),
                ('objectives', models.TextField(blank=True, null=True)),
                ('characters', models.ManyToManyField(related_name='scenes', to='storyapp.character')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenes', to='storyapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('locations', models.ManyToManyField(related_name='worlds', to='storyapp.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]