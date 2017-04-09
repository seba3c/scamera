# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 01:18
from __future__ import unicode_literals

from django.db import migrations


def set_module_name(apps, schema_editor):
    TelegramBot = apps.get_model("notifications", "TelegramBot")

    for tbot in TelegramBot.objects.all():
        tbot.module_name = tbot.name
        tbot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20161014_0113'),
    ]

    operations = [
        migrations.RunPython(set_module_name)
    ]