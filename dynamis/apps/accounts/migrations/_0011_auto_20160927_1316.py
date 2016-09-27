# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-27 10:16
from __future__ import unicode_literals

from django.db import migrations


def move_account_configs(apps, schema_editor):
    AccountConfig = apps.get_model('accounts', 'AccountConfig')
    EthAccount = apps.get_model('payments', 'EthAccount')
    for account_config in AccountConfig.objects.all():
        eth_account, created = EthAccount.objects.get_or_create(user=account_config.user)
        if created:
            eth_account.eth_address = account_config.rpc_node_host
            eth_account.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_user_linkedin_account'),
    ]

    operations = [
        migrations.RunPython(move_account_configs)
    ]
