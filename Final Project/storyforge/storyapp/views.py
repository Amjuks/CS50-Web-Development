from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .helpers import get_user_world_stats
from .models import World

# Create your views here.
class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'storyapp/index.html')
    
class CreateStoryView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'storyapp/create_story.html')
    
class DashboardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        context.update(get_user_world_stats(request.user))

        return render(request, 'storyapp/dashboard.html', context)
    
class StoryboardView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        try:
            context['world'] = World.objects.get(id=world_id)
        except World.DoesNotExist:
            return redirect(reverse('storyapp:dashboard'))

        return render(request, 'storyapp/storyboard_story.html', context)
    
    def post(self, request: HttpRequest, world_id: int) ->  HttpResponse:
        print(request.POST)
        
class StoryboardCharactersView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        try:
            context['world'] = World.objects.get(id=world_id)
        except World.DoesNotExist:
            return redirect(reverse('storyapp:dashboard'))

        return render(request, 'storyapp/storyboard_characters.html', context)
    
class StoryboardLocationsView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        try:
            context['world'] = World.objects.get(id=world_id)
        except World.DoesNotExist:
            return redirect(reverse('storyapp:dashboard'))

        return render(request, 'storyapp/storyboard_locations.html', context)
    
class StoryboardScenesView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        try:
            context['world'] = World.objects.get(id=world_id)
        except World.DoesNotExist:
            return redirect(reverse('storyapp:dashboard'))

        return render(request, 'storyapp/storyboard_scenes.html', context)