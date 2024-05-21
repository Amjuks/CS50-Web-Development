from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("personal", views.personal_view, name="personal"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist_view, name="watchlist"),
    path("bid/<int:listing_id>", views.bid_view, name="bid"),
    path("category/<int:category_id>", views.category_view, name='category'),
    path("comment/<int:listing_id>", views.comment_view, name="comment")
]
