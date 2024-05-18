from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import *

from pprint import pprint as p

class BootStrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CreateListingForm(BootStrapForm):
    title = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'autofocus': True}))
    description = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'rows': 3}))
    starting_price = forms.IntegerField(min_value=0)
    image = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].choices = [(category.id, category.name) for category in Category.objects.all()]
        

class BidForm(BootStrapForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': "Place a bid!"}))

    def __init__(self, *args, **kwargs):
        min_bid = kwargs.pop('min_bid', None)
        super().__init__(*args, **kwargs)

        if min_bid is None:
            self.fields['amount'].widget.attrs['min'] = 1
        else:
            self.fields['amount'].widget.attrs['min'] = min_bid


class CloseAuctionForm(BootStrapForm):

    def __init__(self, listing: Listings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = listing

    def clean(self):
        cleaned_data = super().clean()
        
        if not self.listing.get_highest_bid():
            raise forms.ValidationError("Auction cannot be closed as there are no bids placed")

        return cleaned_data

def index(request):

    return render(request, "auctions/index.html", {
        'listings': Listings.objects.all()
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
        min_bid = listing.highest_bid or listing.starting_price

        if listing.open:
            highest_bid = None
        
        else:
            highest_bid = listing.get_highest_bid()

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": BidForm(min_bid=min_bid),
            "user_in_wishlist": listing.users_wishlist.filter(pk=request.user.pk).exists(),
            "highest_bid": highest_bid
        })

def wishlist_view(request, listing_id=None):

    if not listing_id:
        return render(request, "auctions/wishlist.html")

    if request.method == "POST":
        listing = Listings.objects.get(id=listing_id)
        user = request.user

        if request.user.wishlist_items.filter(id=listing_id).exists():
            user.wishlist_items.remove(listing)
        
        else:
            user.wishlist_items.add(listing)

        return redirect(reverse('listing', args=[listing_id]))
    

def bid_view(request, listing_id):
    listing = Listings.objects.get(id=listing_id)

    if request.method == "POST":
        form = BidForm(request.POST, min_bid=listing.highest_bid)
        
        if form.is_valid():
            amount = form.cleaned_data['amount']
            highest_bid = listing.highest_bid or listing.starting_price

            if amount > highest_bid:
                Bids(
                    user=request.user,
                    listing=listing,
                    amount=amount
                ).save()

                listing.highest_bid = amount
                listing.save()

                return redirect(reverse('listing', args=[listing_id]))

            else:
                form.add_error('amount', 'Your bid must be higher than the current bid.')
                return render(request, 'auctions/listing.html', {'listing': listing, 'bid_form': form})

        else:
            return redirect(reverse('listing', args=[listing_id]))