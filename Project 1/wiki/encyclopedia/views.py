import markdown2

from django.shortcuts import render, redirect
from django.urls import reverse
from . import util


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

    title = request.POST['q'].lower()
    entry = util.get_entry(title)

    if entry is not None:
        return redirect(reverse("entry", args=[title]))

    entries = util.list_entries()

    entries = [entry for entry in entries if title in entry.lower()]

    return render(request, 'encyclopedia/search.html', {
        'title': title,
        'entries': entries
    })