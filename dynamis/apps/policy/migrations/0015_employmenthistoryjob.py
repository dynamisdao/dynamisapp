# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-04 12:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policy', '0014_auto_20161004_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentHistoryJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('company', models.CharField(max_length=255)),
                ('is_current_job', models.BooleanField()),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('date_begin', models.DateField()),
                ('date_end', models.DateField(null=True)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_history_jobs', to='policy.PolicyApplication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_history_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
