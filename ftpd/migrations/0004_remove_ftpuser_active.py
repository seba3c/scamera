# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 03:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ftpd', '0003_ftpdserverconfig_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ftpuser',
            name='active',
        ),
    ]
