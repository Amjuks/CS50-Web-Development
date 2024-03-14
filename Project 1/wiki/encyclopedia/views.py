import markdown2

from random import choice
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput({
        'class': 'search',
        'placeholder': "Search Encyclopedia"
    }))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput({
        'class': "form-control",
        'required': True
    }))

    content = forms.CharField(label="Content", widget=forms.Textarea({
        'class': "form-control content-textarea",
        'required': True
    }))

class EditForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput({
        'class': "form-control",
        'readonly': True
    }))

    content = forms.CharField(label="Content", widget=forms.Textarea({
        'class': "form-control content-textarea",
        'required': True
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

def new(request):

    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            entries = [entry.lower() for entry in util.list_entries()]

            title_exists = title.lower() in entries

            if title_exists:
                form.add_error('title', "This title already exists!")
                print(f'{form.errors = }')
                return render(request, "encyclopedia/new.html", {
                    'form': form
                })
            
            content = f'#{title}\n\n' + form.cleaned_data["content"]
            util.save_entry(title, content)

            return redirect(reverse('entry', args=[title]))
        
        else:
            return render(request, "encyclopedia/new.html", {
                'form': form
            })    

    return render(request, "encyclopedia/new.html", {
        'form': CreateForm()
    })

def edit(request, title):

    if request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"].replace('\r', '') # remove unnecessary "\r" added by browser

            util.save_entry(title, content)

            return redirect(reverse('entry', args=[title]))

        else:
            return render(request, 'encyclopedia/edit.html', {
                'form': form
            })
    
    else:
        content = util.get_entry(title)

        if content:
            form = EditForm({
                'title': title,
                'content': content
            })

            return render(request, "encyclopedia/edit.html", {
                'form': form
            })
        
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "error": "DNE" # Does Not Exist
        })
    
def random(request):

    title = choice(util.list_entries())
    return redirect(reverse('entry', args=[title]))