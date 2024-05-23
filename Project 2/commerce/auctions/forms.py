from django import forms
from .models import Category, Listings

class BootStrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CreateListingForm(BootStrapForm):
    title = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'style': 'height: 7rem', 'placeholder': 'Description'}))
    starting_price = forms.IntegerField(min_value=10, max_value=10**6, widget=forms.NumberInput(attrs={'placeholder': 'Starting Price'}))
    image = forms.URLField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Image URL'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Category", widget=forms.Select(attrs={'class': 'form-select'}))

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
    
class CommentForm(BootStrapForm):
    user_comment = forms.CharField(
        label="Leave a comment!",
        widget=forms.Textarea(attrs={
            'style': 'height:5em;',
            'placeholder': "Leave a comment here!"
        })
    )