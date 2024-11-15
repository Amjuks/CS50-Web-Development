from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .helpers import get_user_world_stats
from .models import World, User, Character, Location, Scene

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
        context = {'success': False}

        try:
            name = request.POST.get('world_name')
            description = request.POST.get('world_description')
            world_cover = request.FILES.get('world_cover')

            world = World.objects.get(id=world_id)
            world.name = name
            world.description = description
            world.world_cover = world_cover
            world.save()

        except Exception as e:
            context['error'] = f"{type(e).__name__}: {e}"
            print(context['error'])

        return redirect(reverse('storyapp:storyboard', kwargs={'world_id': world_id}))

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
    
class CharacterView(View):
    def get(self, request: HttpRequest, world_id: int, name: str) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        context['character'] = Character.objects.get(world=context['world'], name=name)
        return render(request, 'storyapp/character.html', context=context)
    
class LocationView(View):
    def get(self, request: HttpRequest, world_id: int, name: str) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        context['location'] = Location.objects.get(world=context['world'], name=name)
        return render(request, 'storyapp/location.html', context=context)
    
class SceneView(View):
    def get(self, request: HttpRequest, world_id: int, name: str) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        context['scene'] = Scene.objects.get(world=context['world'], title=name)
        return render(request, 'storyapp/scene.html', context=context)
    
class CreateCharacterView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        return render(request, 'storyapp/create_character.html', context=context)
    
class CreateLocationView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        return render(request, 'storyapp/create_location.html', context=context)
    
class CreateSceneView(View):
    def get(self, request: HttpRequest, world_id: int) -> HttpResponse:
        context = {}
        context['world'] = World.objects.get(id=world_id)
        return render(request, 'storyapp/create_scene.html', context=context)

class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'storyapp/login.html')
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("storyapp:dashboard"))
        else:
            return render(request, "storyapp/login.html", {
                "message": "Invalid username and/or password."
            })

class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'storyapp/register.html')
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST["username"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "storyapp/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "storyapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("storyapp:index"))

class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return HttpResponseRedirect(reverse("storyapp:index"))