# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from forms import ContactForm
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Min, Count
import sr.models
import random

def index(request):
    return render(request, 'sr/index.html')

### COPIED OVER
def decks(request):
    if (request.user.is_authenticated()):
        instance_list = sr.models.DeckInstance.objects.filter(user=request.user)
        count_list = [len(sr.models.ScheduledReview.objects.filter(deck_instance=x).filter(when_due__lt=datetime.datetime.now())) for x in instance_list]
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
            sr.models.ContactForm.objects.create(email=form.cleaned_data['email'],
                                              subject=form.cleaned_data['subject'],
                                              message=form.cleaned_data['message'])
        else:
            success = False
    return render(request, 'sr/contact.html', {'form': ContactForm(), 'success': success})

def contact_success(request):
    return render(request, 'sr/contact-success.html')

def browse_decks(request):
    added = {}
    if (request.user.is_authenticated()):
        added = {di.deck for di in sr.models.DeckInstance.objects.filter(user=request.user)}
    notAdded = [d for d in sr.models.Deck.objects.all() if d not in added]
    added = list(added)
    countsAdded = [len(sr.models.Card.objects.filter(deck=d)) for d in added]
    countsNotAdded = [len(sr.models.Card.objects.filter(deck=d)) for d in notAdded]
    return render(request, 'sr/browse-decks.html', {'added': added, 'notAdded': notAdded, 'countsAdded': countsAdded,
                                                    'countsNotAdded': countsNotAdded})

def add_deck(request, deck_name):
    decks = sr.models.Deck.objects.filter(name=deck_name)
    if not decks:
        raise Http404("No deck with name \"" + deck_name + "\" exists.")
    if (request.user.is_authenticated()):
        di = sr.models.DeckInstance(deck=decks[0], user=request.user, scheduler=None)
        # if user attempts to add duplicate deck instance, update nothing
        try:
            di.save()
            for c in sr.models.Card.objects.filter(deck=di.deck):
                newReview = sr.models.ScheduledReview(card=c, deck_instance=di, when_due=datetime.datetime.now())
                newReview.save()
        except IntegrityError:
            pass
        return HttpResponseRedirect(reverse('sr:decks'))
    else:
        return HttpResponseRedirect(reverse('sr:login'))

def review(request, deck_name):
    if request.user.is_authenticated():
        try:
            d = sr.models.Deck.objects.get(name=deck_name)
            di = sr.models.DeckInstance.objects.get(user=request.user, deck=d)
        except ObjectDoesNotExist:
            raise Http404("Currently you do not have access to deck \"" + deck_name + "\".")
        if request.method == 'POST':
            try:
                rev = sr.models.ScheduledReview.objects.get(pk=int(request.POST['id']))
                return HttpResponse(str(rev) + ' ' + str(rev.id))
            except (ValueError, ObjectDoesNotExist):
                raise HttpResponseBadRequest('Invalid form input.')
            
            # update db 
        rev = sr.models.ScheduledReview.objects.filter(deck_instance=di, done=False).earliest('when_due')
        #card = sr.models.Card(front="Front test", back="Reverse test", deck=d)
        return render(request, 'sr/review.html', {'card': rev.card, 'id': rev.pk})
    else:
        return HttpResponseRedirect(reverse('sr:login'))

def getting_started(request):
    return render(request, 'sr/getting-started.html')

def deck_details(request, deck_name):
    matches = sr.models.Deck.objects.filter(name=deck_name)
    if not matches:
        raise Http404("No deck with name \"" + deck_name + "\" exists.")
    return render(request, 'sr/deck-details.html', {'deck': matches[0]})
