# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 04:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sr', '0002_auto_20170811_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='finishedreview',
            name='answer',
        ),
        migrations.AddField(
            model_name='deckinstance',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='finishedreview',
            name='score',
            field=models.CharField(choices=[('WR', 'Incorrect'), ('HR', 'Correct but with difficult'), ('EZ', 'Correct and easy')], default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deckinstance',
            name='scheduler',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sr.Scheduler'),
            preserve_default=False,
        ),
    ]
