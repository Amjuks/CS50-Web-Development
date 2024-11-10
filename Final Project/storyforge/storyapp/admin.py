from django.contrib import admin

from storyapp.models import User, Character, Relationship, Location, World, Scene

# # Register your models here.
admin.site.register(User)
admin.site.register(Character)
admin.site.register(Relationship)
admin.site.register(Location)
admin.site.register(World)
admin.site.register(Scene)