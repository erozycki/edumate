# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-20 02:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sr', '0009_contactform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactform',
            old_name='from_email',
            new_name='email',
        ),
    ]
