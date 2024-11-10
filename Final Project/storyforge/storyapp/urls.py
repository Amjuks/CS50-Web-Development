from django.urls import path

from . import views

app_name = 'storyapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('create/', views.CreateStoryView.as_view(), name='create-story'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('storyboard/<int:world_id>/', views.StoryboardView.as_view(), name='storyboard'),
    path('storyboard/<int:world_id>/characters', views.StoryboardCharactersView.as_view(), name='storyboard-characters'),
    path('storyboard/<int:world_id>/locations', views.StoryboardLocationsView.as_view(), name='storyboard-locations'),
    path('storyboard/<int:world_id>/scenes', views.StoryboardScenesView.as_view(), name='storyboard-scenes'),

    path('storyboard/<int:world_id>/characters/create', views.CreateCharacterView.as_view(), name='create-character'),
    path('storyboard/<int:world_id>/locations/create', views.CreateLocationView.as_view(), name='create-location'),
    path('storyboard/<int:world_id>/scenes/create', views.CreateSceneView.as_view(), name='create-scene'),
    
    path('storyboard/<int:world_id>/characters/<str:name>', views.CharacterView.as_view(), name='character'),
    path('storyboard/<int:world_id>/locations/<str:name>', views.LocationView.as_view(), name='location'),
    path('storyboard/<int:world_id>/scenes/<str:name>', views.SceneView.as_view(), name='scene'),
]