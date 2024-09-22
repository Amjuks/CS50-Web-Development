import json
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, OuterRef, Exists
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import View

from .helpers import format_datetime
from .models import User, Post, Like, Follow
from .constants import POST_CREATION_PROMPTS

POSTS_PER_PAGE = 10

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@method_decorator(login_required, name="dispatch")
class PostsAPIView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {'success': False}
        page = request.GET.get('page')
        follower = request.GET.get('follower')

        page = int(page) if page else 1

        if not follower:
            profile_user = request.GET.get('profile_user')

        try:
            if follower:
                follower = User.objects.get(id=follower)
                following = Follow.objects.filter(follower=follower)
                following = [follow.following for follow in following]

                posts = Post.objects.filter(creator__in=following)

            elif profile_user:
                posts = Post.objects.filter(creator__id=profile_user)

            else:
                posts = Post.objects.all()


            has_liked_subquery = Like.objects.filter(
                user=request.user,
                post=OuterRef('pk')
            ).values('id')

            posts = posts.annotate(
                likes_count=Count('likes'),
                has_liked=Coalesce(Exists(has_liked_subquery), False)
            ).order_by('-created_at')

            page = Paginator(posts, POSTS_PER_PAGE, error_messages={"no_results": "Page does not exist"}).get_page(page)

            context['posts'] = [
                {
                    'id': post.id,
                    'creator': post.creator.username,
                    'content': post.content,
                    'created_at': format_datetime(post.created_at),
                    'likes_count': post.likes_count,
                    'has_liked': post.has_liked,
                }
                for post in page
            ]

            context['has_previous'] = page.has_previous()
            context['has_next'] = page.has_next()
            context['page'] = page.number

            context['success'] = True

        except Exception as e:
            context['error'] = f"{type(e).__name__}: {e}"
            print(context['error'])

        return JsonResponse(context)

@method_decorator(login_required, name="dispatch")
class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}

        has_liked_subquery = Like.objects.filter(
            user=request.user,
            post=OuterRef('pk')
        ).values('id')

        context['posts'] = Post.objects.all().annotate(
            likes_count=Count('likes'),
            has_liked=Coalesce(Exists(has_liked_subquery), False)
        )

        return render(request, "network/index.html", context)
    
@method_decorator(login_required, name="dispatch")
class CreateView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        context['header'], context['placeholder'] = random.choice(POST_CREATION_PROMPTS)
        
        return render(request, 'network/create.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        context = {'success': False}
        data = json.loads(request.body)
        content = data['content']

        try:
            Post.objects.create(creator=request.user, content=content).save()

            # Change to Profile Redirect
            context['success'] = True
        
        except Exception as e:
            context['error'] = f"{type(e).__name__}: {e}"
            print(context['error'])

        return JsonResponse(context)

@method_decorator(login_required, name="dispatch")
class ProfileView(View):

    def get(self, request, user: str):
        context = {}
        user = User.objects.get(username=user)
        context['profile_user'] = user
        context['follower_count'] = user.follower.all().count()
        context['following_count'] = user.following.all().count()

        has_liked_subquery = Like.objects.filter(
            user=request.user,
            post=OuterRef('pk')
        ).values('id')

        context['posts'] = Post.objects.filter(creator=user).annotate(
            likes_count=Count('likes'),
            has_liked=Coalesce(Exists(has_liked_subquery), False)
        )

        context['post_count'] = context["posts"].count()
        
        try:
            context['follows'] = Follow.objects.get(follower=request.user, following=user)
        except Follow.DoesNotExist:
            context['follows'] = False
        
        return render(request, 'network/profile.html', context)
    
@method_decorator(login_required, name="dispatch")
class FollowingPostsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'network/following.html')

@method_decorator(login_required, name="dispatch")
class EditPostView(View):
    def get(self, request: HttpRequest, post_id: int) -> HttpResponse:
        context = {}
        context['post'] = Post.objects.get(id=post_id)

        if context['post'].creator != request.user:
            return redirect(reverse('index'))

        return render(request, 'network/edit_post.html', context)
    
    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        context = {'success': False}
        data = json.loads(request.body)

        try:
            post = Post.objects.get(id=post_id)

            if not post.creator == request.user:
                raise Exception("You do not have access to edit this post")
            
            post.content = data['content']
            post.save()

            context['success'] = True
            
        except Post.DoesNotExist:
            context['error'] = "Post does not exist"
        
        except Exception:
            context['error'] = "Post does not exist"

        return JsonResponse(context)

@method_decorator(login_required, name="dispatch")
class LikeView(View):

    def post(self, request: HttpRequest) -> HttpResponse:
        context = {'success': False}
        data = json.loads(request.body)
        post_id = data['post']
        liked = data['liked']

        try:
            post = Post.objects.get(id=post_id)
            if liked:
                Like.objects.get_or_create(user=request.user, post=post)
            else:
                Like.objects.filter(user=request.user, post=post).delete()
            
            context['count'] = Like.objects.filter(post=post).count()
            context['success'] = True

        except Post.DoesNotExist:
            context['error'] = "Post does not exist"

        return JsonResponse(context)
    
@method_decorator(login_required, name="dispatch")
class FollowView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        context = {'success': False}
        data = json.loads(request.body)
        print(f"{data = } ")
        profile_user = User.objects.get(id=data['profileUser'])
        follow_action = data['followAction']

        try:
            if follow_action:
                Follow.objects.get_or_create(follower=request.user, following=profile_user)
                context['follow_action'] = True
            else:
                try:
                    Follow.objects.get(follower=request.user, following=profile_user).delete()
                except Follow.DoesNotExist:
                    ...
                
                context['follow_action'] = False
            
            context['follow_count'] = Follow.objects.filter(following=profile_user).count()
            context['success'] = True

        except Exception as e:
            context['error'] = f"{type(e).__name__}: {e}"
            print(context['error'])

        return JsonResponse(context)