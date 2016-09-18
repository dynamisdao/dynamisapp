# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-08 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policy', '0008_policyapplication_is_signed'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskAssessmentTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('bet1', models.FloatField(null=True)),
                ('bet2', models.FloatField(null=True)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessment_task', to='policy.PolicyApplication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessment_task', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]