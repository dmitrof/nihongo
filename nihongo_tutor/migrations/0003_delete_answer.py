# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 12:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nihongo_tutor', '0002_answer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
