# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-14 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20161014_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambot',
            name='debug',
            field=models.BooleanField(default=False),
        ),
    ]