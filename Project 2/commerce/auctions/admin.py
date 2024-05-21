from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import *

class ListingsAdminForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 50, 'style': 'resize: vertical; height:auto;'})
        }

class WatchlistInline(admin.TabularInline):
    model = Listings.users_watchlist.through
    verbose_name = "Watchlist User"
    verbose_name_plural = "Watchlist Users"
    extra = 0

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):

    # main interface
    list_display = ['user', 'formatted_listing', 'formatted_amount', 'created']

    def formatted_listing(self, obj):
        return obj.listing.title
    
    def formatted_amount(self, obj):
        return f'${obj.amount}'
    
    formatted_listing.short_description = 'Listing'
    formatted_amount.short_description = 'Amount'

    # individual interface
    readonly_fields = ['created']
    fieldsets = (
        ('Bid Information', {
            'fields': ('user', 'listing', 'amount', 'created')
        }),
    )

    
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password',  'is_superuser', 'is_active'),
        }),
    )

    filter_horizontal = ()


@admin.register(Listings)
class ListingsAdmin(admin.ModelAdmin):

    # main interface
    list_display = ['id', 'title', 'owner', 'starting_price', 'highest_bid', 'open', 'created']
    list_filter = ['open', 'created']
    search_fields = ['title', 'owner__username']
    readonly_fields = ['id', 'created']
    ordering = ['id']

    # individual interface
    form = ListingsAdminForm
    readonly_fields = ('created', 'id')
    fieldsets = (
        ('Basic Information', {
            'fields': (('title', 'open'), 'description', 'image', 'category')
        }),
        ('Pricing Information', {
            'fields': (('starting_price', 'highest_bid'),)
        }),
        ('Owner and Timestamps', {
            'fields': (('owner', 'created'), 'id')
        }),
    )
    
    inlines = [WatchlistInline]
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # main interface
    list_display = ['id', 'name', 'color_display']
    ordering = ['id']

    # individual interface
    readonly_fields = ('id', )

    def color_display(self, obj):
        color_hex = "#{:06x}".format(obj.color)  # Convert color to hex format
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', color_hex)
    
    color_display.short_description = 'Color'
    color_display.allow_tags = True

# Register your models here.
admin.site.register(Comments)
# admin.site.register(Watchlist)