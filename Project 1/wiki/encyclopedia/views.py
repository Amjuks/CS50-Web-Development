import markdown2

from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput({
        'class': 'search',
        'placeholder': "Search Encyclopedia"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    entry = util.get_entry(title)
    
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "error": "DNE" # Does Not Exist
        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry)
        })
        
def search(request):

    if request.method == 'POST':
        
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['q']
            entry = util.get_entry(title)

            if entry is not None:
                return redirect(reverse("entry", args=[title]))

            entries = util.list_entries()

            return render(request, 'encyclopedia/search.html', {
                'title': title,
                'entries': [entry for entry in entries if title in entry.lower()]
            })
        
    return redirect(reverse('index'))