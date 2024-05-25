from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *
from humanize import naturaltime

from pprint import pprint as p


def index(request):

    return render(request, "auctions/index.html", {
        'listings': Listings.objects.all()
    })

def personal_view(request):

    if not request.user.is_authenticated:
        return redirect(reverse('index'))
    
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.filter(owner=request.user)
    })
    

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_view(request):

    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_price = form.cleaned_data["starting_price"]
            image_url = form.cleaned_data.get("image", None)
            category = form.cleaned_data["category"]

            listing = Listings(
                owner=request.user,
                title=title,
                description=description,
                starting_price=starting_price,
                image=image_url,
                category=category
            )
            
            listing.save()

            return redirect(reverse("listing", args=[listing.id]))

    else:
        return render(request, "auctions/create.html", {
            'form': CreateListingForm()
        })
    
def listing_view(request, listing_id):

    listing = Listings.objects.get(id=listing_id)
    
    if request.method == 'POST':
        form = CloseAuctionForm(listing, request.POST)

        if form.is_valid():
            listing.open = False
            listing.save()

            return redirect(reverse('listing', args=(listing_id,)))
        else:
            error = form.non_field_errors()
            error = error[0] if error else None
            
            min_bid = listing.highest_bid or listing.starting_price
            bid_form = BidForm(min_bid=min_bid)

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_form": bid_form,
                "error": error,
                "highest_bid": listing.get_highest_bid()
            })

    else:

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user_in_watchlist": listing.users_watchlist.filter(pk=request.user.pk).exists(),
            "bids": Bids.objects.filter(listing_id=listing_id).order_by('-created'),
            "comments": Comments.objects.filter(listing_id=listing_id).order_by('-created')
        })

def watchlist_view(request):

    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = Listings.objects.get(id=listing_id)
        user = request.user

        if user.watchlist_items.filter(id=listing_id).exists():
            user.watchlist_items.remove(listing)
        
        else:
            user.watchlist_items.add(listing)

        return JsonResponse({'success': True, 'action': 'watchlist'})
    
    return render(request, "auctions/index.html", {
        'listings': request.user.watchlist_items.all()
    })
    

def close_view(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = Listings.objects.get(id=listing_id)
        response = {'success': True, 'action': 'close'}

        if not listing.highest_bid:
            response['success'] = False
            response['message'] = "You can't close an auction with no bids"
            return JsonResponse(response)

        listing.open = False
        listing.save()

        return JsonResponse(response)

def bid_view(request):

    if request.method == "POST":
        bid_amount = int(request.POST.get('bid_amount'))
        listing = Listings.objects.get(id=request.POST.get('listing_id'))
        highest_bid = listing.highest_bid

        if not listing.open:
            return JsonResponse({
                'success': False,
                'message': "Auction is closed"
            })
        
        if not highest_bid:
            highest_bid = listing.starting_price - 1

        if highest_bid >= bid_amount:
            return JsonResponse({
                'success': False,
                'message': f"Your bid must be greater than ${highest_bid}",
            })

        bid = Bids(
            user=request.user,
            listing=listing,
            amount=bid_amount
        )
        listing.highest_bid = bid.amount

        bid.save()
        listing.save()

        return JsonResponse({
            'success': True,
            'bid': {'user': request.user.username, 'amount': bid.amount},
            'time': naturaltime(bid.created)
        })
    
    return JsonResponse({'success': False, 'message': "Invalid request"})
        
def category_view(request, category_id):
    
    category = Category.objects.get(id=category_id)

    return render(request, "auctions/index.html", {
        'category': category.name.capitalize(),
        'listings': Listings.objects.filter(category__id=category_id)
    })

def comment_view(request, listing_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            user_comment: str = form.cleaned_data["user_comment"]
            Comments(
                user=request.user,
                listing=Listings.objects.get(id=listing_id),
                content=user_comment
            ).save()

            return redirect(reverse('listing', args=(listing_id,)))