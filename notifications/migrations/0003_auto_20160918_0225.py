# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20160918_0220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrambot',
            name='id',
        ),
        migrations.AlterField(
            model_name='telegrambot',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='telegrambot',
            name='token',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
