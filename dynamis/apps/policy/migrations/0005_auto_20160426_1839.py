# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-26 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0004_auto_20160422_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peerreview',
            name='data',
            field=models.TextField(default='{}'),
        ),
    ]
