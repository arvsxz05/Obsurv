# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey_questions',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]