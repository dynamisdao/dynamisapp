# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0005_auto_20160426_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peerreview',
            name='is_final',
        ),
        migrations.AlterField(
            model_name='peerreview',
            name='data',
            field=models.TextField(),
        ),
    ]
