# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-02 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0007_auto_20160428_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='policyapplication',
            name='is_signed',
            field=models.BooleanField(default=False),
        ),
    ]