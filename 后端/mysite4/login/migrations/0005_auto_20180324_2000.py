# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-24 12:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='user_phone',
        ),
    ]
