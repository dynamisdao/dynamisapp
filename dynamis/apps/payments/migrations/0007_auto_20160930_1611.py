# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-30 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def delete_test_old_smart_deposits(apps, schema_editor):
    SmartDeposit = apps.get_model('payments', 'SmartDeposit')
    for smart_deposit in SmartDeposit.objects.all():
        if smart_deposit.user.policies.exists():
            smart_deposit.policy = smart_deposit.user.polisies.first
            smart_deposit.save()


class Migration(migrations.Migration):
    dependencies = [
        ('policy', '0013_auto_20160923_2114'),
        ('payments', '0006_auto_20160930_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartdeposit',
            name='policy',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='smart_deposit', to='policy.PolicyApplication'),
            preserve_default=False,
        ),
        migrations.RunPython(delete_test_old_smart_deposits),
        migrations.RemoveField(
            model_name='smartdeposit',
            name='user',
        ),
    ]
