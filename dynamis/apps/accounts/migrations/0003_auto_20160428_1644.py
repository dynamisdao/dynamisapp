# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_verified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='keybase_username',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='keybase_verified',
            field=models.BooleanField(default=False),
        ),
    ]