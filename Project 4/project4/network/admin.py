from django import forms
from django.contrib import admin

from .models import User, Follow, Post, Like, Comment
    
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    ...

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ...

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ...

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...