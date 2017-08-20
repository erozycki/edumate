# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100, default="Orphaned", db_index=True, unique=True)
    description = models.TextField(default="")
    last_added_to = models.DateTimeField(auto_now_add=True)
    last_modified_content = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Card(models.Model):
    front = models.TextField()
    back = models.TextField()
    deck = models.ForeignKey(Deck, db_index=True)
    when_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=200, blank=True, default="")
    def __str__(self):
        if self.summary:
            return self.summary
        return self.front[:200]

class Scheduler(models.Model):
    name = models.CharField(max_length=100)
    ref = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CardRelationsSchema(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=200, blank=True, default='')
    blob = models.BinaryField(blank=True, null=True, default=None)
    def __str__(self):
        return self.name

class CardRelationsSet(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    schema = models.ForeignKey(CardRelationsSchema)
    deck = models.ForeignKey(Deck)
    last_modified = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=200, blank=True, default='')
    blob = models.BinaryField(blank=True, null=True, default=None)
    def __str__(self):
        return self.deck.name + ": " + self.schema.name

class DeckInstance(models.Model):
    deck = models.ForeignKey(Deck, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    when_created = models.DateTimeField(auto_now_add=True)
    scheduler = models.ForeignKey(Scheduler)
    card_relations_set = models.ForeignKey(CardRelationsSet, blank=True, null=True)
    reviews_done = models.IntegerField()
    def __str__(self):
        return self.deck.name + "; " + self.user.username

class ScheduledReview(models.Model):
    card = models.ForeignKey(Card, db_index=True)
    deck_instance = models.ForeignKey(DeckInstance, db_index=True)
    when_scheduled = models.DateTimeField(auto_now_add=True, db_index=True)
    when_due = models.DateTimeField(db_index=True)
    def __str__(self):
        return "Card in " + self.deck_instance.deck + " due on " + self.when_due

class FinishedReview(models.Model):
    scheduled_review = models.ForeignKey(ScheduledReview)
    WRONG = 'WR'
    HARD = 'HR'
    EASY =  'EZ'
    SCORE_CHOICES = (
        (WRONG, "Incorrect"),
        (HARD, "Correct but with difficult"),
        (EASY, "Correct and easy"),
    )
    score = models.CharField(max_length=2, choices=SCORE_CHOICES)
    answer_long_form = models.TextField(blank=True, default='')
    when_reviewed = models.DateTimeField(auto_now_add=True, db_index=True)
    def __str__(self):
        return ("Card in " + self.scheduled_review.deck_instance.deck + " reviewed on " + 
                self.when_reviewed + ": " + self.score)

# hack to be used until mail server is set up
class ContactForm(models.Model):
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    def __str__(self):
        return subject
