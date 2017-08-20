# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sr', '0003_auto_20170811_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishedreview',
            name='when_reviewed',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='scheduledreview',
            name='when_due',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='scheduledreview',
            name='when_scheduled',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
