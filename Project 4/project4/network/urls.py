
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("profile/<str:user>/", views.ProfileView.as_view(), name="profile"),
    path("following/", views.FollowingPostsView.as_view(), name="following"),
    path("post/edit/<int:post_id>/", views.EditPostView.as_view(), name="post-edit"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("like/", views.LikeView.as_view(), name="like"),
    path("follow/", views.FollowView.as_view(), name="follow"),

    path("api/posts/", views.PostsAPIView.as_view(), name="api-posts"),
]
