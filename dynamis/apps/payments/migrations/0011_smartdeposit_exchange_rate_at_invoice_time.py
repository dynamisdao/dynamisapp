# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-07 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_auto_20161007_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartdeposit',
            name='exchange_rate_at_invoice_time',
            field=models.FloatField(null=True),
        ),
    ]