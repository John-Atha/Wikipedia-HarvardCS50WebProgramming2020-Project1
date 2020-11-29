import sys
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
import random
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    information = forms.CharField(widget=forms.Textarea(), label="Markdown Content")

class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    information = forms.CharField(widget=forms.Textarea(), label="Markdown Content")


def substring(search_term, x):
    return search_term in x


def search(request):
    entries = util.list_entries()
    search_term = ''
    if 'q' in request.GET:
        search_term = request.GET['q']
        if search_term in entries:
            return display(request, search_term)
        else:        
            results = filter( lambda x: substring(search_term, x), entries )
            if results:
                return render(request, "encyclopedia/results_page.html", {
                    "results" : results
                })
            else:
                return render(request, "encyclopedia/results_error.html")
                


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return display(request, title)



def edit(request):
    title = request.POST.get("key")
    details = util.get_entry(title)
    form = EditEntryForm(initial={'information': details, 'title':title})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
        })



def save(request):
    old_title = request.POST.get("old_title")
    entries = util.list_entries()
    form = EditEntryForm(request.POST)
    if form.is_valid():
        title=form.cleaned_data["title"]
        info=form.cleaned_data["information"]
        util.replace(old_title, title, info)
        return display(request, title)
    else:
        return index(request)



def add(request):
    # if i am trying to add a task
    if request.method == "POST":
        # an item of the form class, with the data of the request
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["information"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create_error.html")
            else:
                util.add(title, info)
                return render(request, "encyclopedia/display.html", {
                    "details": markdown2.markdown(util.get_entry(title)),
                    "title": title
                    } )
        else : return render(request, "encyclopedia/add.html", {
            "form": form
        })
    return render(request, "encyclopedia/add.html", {
        "form":NewEntryForm
    })


def create_error(requset):
    return render(request, "encyclopedia/create_error.html")

def display(request, title1):
    if title1 not in util.list_entries():
        return render(request, "encyclopedia/error-page.html")
    else:
            return render(request, "encyclopedia/display.html", {
                "details": markdown2.markdown(util.get_entry(title1)),
                "title": title1
                } )



