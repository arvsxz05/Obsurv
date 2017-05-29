# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polls', '0006_survey_questions_card_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey_questions',
            name='card_color',
            field=models.CharField(choices=[('#D98880', 'red'), ('#F1948A', 'pink'), ('#C39BD3', 'purple'), ('#BB8FCE', 'violet'), ('#7FB3D5', 'blue'), ('#85C1E9', 'light-blue'), ('#76D7C4', 'light-blue-green'), ('#73C6B6', 'blue-green'), ('#7DCEA0', 'green'), ('#82E0AA', 'light-green'), ('#F7DC6F', 'yellow'), ('#F8C471', 'yellow-orange'), ('#F0B27A', 'light-orange'), ('#E59866', 'orange')], default='#D98880', max_length=7),
        ),
    ]
