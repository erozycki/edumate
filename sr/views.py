# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from forms import ContactForm

import models

def index(request):
    return render(request, 'sr/index.html')

### COPIED OVER
def decks(request):
    if (request.user.is_authenticated()):
        instance_list = models.DeckInstance.objects.filter(user=request.user)
        return render(request, 'sr/decks.html', {'instance_list': instance_list})
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
    return render(request, 'sr/browse-decks.html')
