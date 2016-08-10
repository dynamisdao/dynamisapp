# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 18:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0006_auto_20160428_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 28, 18, 27, 17, 877442, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicationitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 28, 18, 27, 21, 541658, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peerreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 28, 18, 27, 25, 573426, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peerreview',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 28, 18, 27, 29, 397689, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='policyapplication',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 28, 18, 27, 32, 749787, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='policyapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 28, 18, 27, 36, 77679, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
