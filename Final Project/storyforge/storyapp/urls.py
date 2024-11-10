from django.urls import path

from . import views

app_name = 'storyapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateStoryView.as_view(), name='create-story'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('storyboard/<int:world_id>/', views.StoryboardView.as_view(), name='storyboard'),
    path('storyboard/<int:world_id>/characters', views.StoryboardCharactersView.as_view(), name='storyboard-characters'),
    path('storyboard/<int:world_id>/locations', views.StoryboardLocationsView.as_view(), name='storyboard-locations'),
    path('storyboard/<int:world_id>/scenes', views.StoryboardScenesView.as_view(), name='storyboard-scenes'),
]