# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-05 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160428_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_risk_assessor',
            field=models.BooleanField(default=False),
        ),
    ]
