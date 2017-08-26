# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from forms import ContactForm
from django.db import IntegrityError
import datetime
import models

def index(request):
    return render(request, 'sr/index.html')

### COPIED OVER
def decks(request):
    if (request.user.is_authenticated()):
        instance_list = models.DeckInstance.objects.filter(user=request.user)
        count_list = {x: len(models.ScheduledReview.objects.filter(deck_instance=x).filter(when_due__gt=datetime.datetime.now())) for x in instance_list}
        return render(request, 'sr/decks.html', {'instance_list': instance_list, 'count_list': count_list})
    else:
        return HttpResponseRedirect(reverse('sr:login'))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('sr:decks'))

    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def why_edumate(request):
    return render(request, 'sr/why-edumate.html')

def contact(request):
    success = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True
            models.ContactForm.objects.create(email=form.cleaned_data['email'],
                                              subject=form.cleaned_data['subject'],
                                              message=form.cleaned_data['message'])
        else:
            success = False
    return render(request, 'sr/contact.html', {'form': ContactForm(), 'success': success})

def contact_success(request):
    return render(request, 'sr/contact-success.html')

def browse_decks(request):
    if (request.user.is_authenticated()):
        added = {di.deck for di in models.DeckInstance.objects.filter(user=request.user)}
    not_added = {d for d in models.Deck.objects.all() if d not in added}
    return render(request, 'sr/browse-decks.html', {'added': added, 'not_added': not_added})
#        return render(request, 'sr/decks.html', {'instance_list': instance_list, 'count_list': count_list})
#    else:
#        return HttpResponseRedirect(reverse('sr:login'))

#def browse_decks(request):
#
#    return render(request, 'sr/browse-decks.html')

def add_deck(request, deck_name):
    decks = models.Deck.objects.filter(name=deck_name)
    if not decks:
        raise Http404("No deck with name \"" + deck_name + "\" exists.")
    if (request.user.is_authenticated()):
        di = models.DeckInstance(deck=decks[0], user=request.user, scheduler=None)
        # if user attempts to add duplicate deck instance, update nothing
        try:
            di.save()
        except IntegrityError:
            pass
        return HttpResponseRedirect(reverse('sr:decks'))
    else:
        return HttpResponseRedirect(reverse('sr:login'))

def getting_started(request):
    return render(request, 'sr/getting-started.html')

def deck_details(request, deck_name):
    matches = models.Deck.objects.filter(name=deck_name)
    if not matches:
        raise Http404("No deck with name \"" + deck_name + "\" exists.")
    return render(request, 'sr/deck-details.html', {'deck': matches[0]})

from django.contrib.staticfiles.views import serve
def ssl_validation(request):
    with open('/opt/bitnami/apps/django/django_projects/Project/A74E04808631445013DE8BEC11187C75.txt', 'rb') as f:
        response = HttpResponse(f, content_type="text/plain")
        #response["Content-disposition"] = "attachment
        return response
#    return HttpResponseRedirect(reverse('sr:login'))
#    return serve(request, '/opt/bitnami/apps/django/django_projects/Project/C06F6C31FEB8E0E0454C35722593BC00.txt', '/')
#    return serve(request, 'C06F6C31FEB8E0E0454C35722593BC00.txt')
#    test_file = open('/opt/bitnami/apps/django/django_projects/Project/C06F6C31FEB8E0E0454C35722593BC00.txt', 'rb')
#    response = HttpResponse(content=test_file)
#    response['Content-Type'] = 'application/txt'
#    response['Content-Disposition'] = 'attachment; filename="C06F6C31FEB8E0E0454C35722593BC00.txt"', 
#    return response
