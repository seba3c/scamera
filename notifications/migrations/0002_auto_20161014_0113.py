# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambot',
            name='module_name',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='telegrambot',
            name='name',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
        ),
    ]
