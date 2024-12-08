from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
class World(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worlds')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    world_cover = models.ImageField(upload_to='world_cover_images/', null=True, blank=True)
    public = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    backstory = models.TextField(null=True, blank=True)
    traits = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to='characters/', null=True, blank=True)

    def __str__(self):
        age = f' ({self.age})' if self.age else ''
        return self.name + age
    
class Relationship(models.Model):
    character = models.ForeignKey(Character, related_name='relationships', on_delete=models.CASCADE)
    related_character = models.ForeignKey(Character, related_name='related_to', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.character.name} - {self.related_character.name} ({self.type.capitalize()})"
    
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    significance = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='locations/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Scene(models.Model):
    title = models.CharField(max_length=100)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='scenes')
    location = models.ForeignKey(Location, related_name='scenes', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    objectives = models.JSONField(null=True, blank=True)
    characters = models.ManyToManyField(Character, related_name='scenes', blank=True)

    def __str__(self):
        return f"{self.title} at {self.location.name}"