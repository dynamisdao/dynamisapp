# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-06 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20160930_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartdeposit',
            name='coast',
            field=models.FloatField(null=True),
        ),
    ]