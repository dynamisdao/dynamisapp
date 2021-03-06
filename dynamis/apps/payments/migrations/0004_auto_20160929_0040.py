# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-28 21:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0003_auto_20160927_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyTokenOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FillEthOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellTokenOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SmartDepositRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TokenAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('immature_tokens_balance', models.FloatField(default=0.0)),
                ('mature_tokens_balance', models.FloatField(default=0.0)),
                ('disabled', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='token_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WithdrawalEthOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='fillethaccountoperation',
            name='eth_account',
        ),
        migrations.RenameField(
            model_name='ethaccount',
            old_name='immature_tokens_balance',
            new_name='eth_balance',
        ),
        migrations.RemoveField(
            model_name='ethaccount',
            name='mature_tokens_balance',
        ),
        migrations.RemoveField(
            model_name='premiumpayment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='smartdeposit',
            name='refunded',
        ),
        migrations.RemoveField(
            model_name='smartdeposit',
            name='user',
        ),
        migrations.AddField(
            model_name='premiumpayment',
            name='eth_account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='premium_payments', to='payments.EthAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smartdeposit',
            name='eth_account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='smart_deposits', to='payments.EthAccount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ethaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eth_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FillEthAccountOperation',
        ),
        migrations.AddField(
            model_name='withdrawalethoperation',
            name='eth_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_eth_operations', to='payments.EthAccount'),
        ),
        migrations.AddField(
            model_name='smartdepositrefund',
            name='smart_deposit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smart_deposit_refunds', to='payments.SmartDeposit'),
        ),
        migrations.AddField(
            model_name='selltokenoperation',
            name='eth_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_token_operations', to='payments.EthAccount'),
        ),
        migrations.AddField(
            model_name='selltokenoperation',
            name='token_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_token_operations', to='payments.TokenAccount'),
        ),
        migrations.AddField(
            model_name='fillethoperation',
            name='eth_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fill_eth_operations', to='payments.EthAccount'),
        ),
        migrations.AddField(
            model_name='buytokenoperation',
            name='eth_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_token_operations', to='payments.EthAccount'),
        ),
        migrations.AddField(
            model_name='buytokenoperation',
            name='token_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_token_operations', to='payments.TokenAccount'),
        ),
    ]
