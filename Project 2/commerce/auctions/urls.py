from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("wishlist/<int:listing_id>", views.wishlist_view, name="wishlist"),
    path("bid/<int:listing_id>", views.bid_view, name="bid")
]
