# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 02:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ftpd', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=10)),
                ('telegram_username', models.CharField(max_length=20)),
                ('telegram_bot_id', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramNotificationHandler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('ftp_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftpd.FTPUser')),
                ('subscribers', models.ManyToManyField(blank=True, to='notifications.NotificationUserProfile')),
                ('telegram_bot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notifications.TelegramBot')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
