# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-04 10:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0013_auto_20160923_2114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApplicationItem',
            new_name='ReviewTask',
        ),
    ]
