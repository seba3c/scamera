# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-17 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peopledetectortest',
            name='negative_samples_dir',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='peopledetectortest',
            name='positive_samples_dir',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
