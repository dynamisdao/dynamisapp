# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-06 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0016_auto_20161005_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='policyapplication',
            name='how_long_stay_answer',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Less than 1 year'), (1, 'In about 1 year'), (2, 'Before the end of next year'), (3, 'Maybe before 2 years time'), (4, 'More than 2 years'), (5, 'I love my job. I will work for my present employer till the day I die.')], null=True),
        ),
        migrations.AddField(
            model_name='policyapplication',
            name='unemployment_period_answer',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Maybe 3 weeks to 1 month'), (1, 'Perhaps 1 to 2 months'), (2, 'Possibly 2 to 3 months'), (3, 'Potentially 3 to 4 months'), (4, 'I will need more than 4 months of coverage.')], null=True),
        ),
        migrations.AlterField(
            model_name='policyapplication',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(1, 'init'), (2, 'submitted_wait_for_deposit'), (3, 'on_p2p_review'), (10, 'on_completeness_check'), (4, 'on_risk_assessment_review'), (5, 'approved'), (6, 'on_smart_deposit_refund'), (7, 'deleted'), (8, 'active'), (9, 'wait_for_premium')], default=1, protected=True),
        ),
    ]
