# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20160918_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationuserprofile',
            name='telegram_username',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]