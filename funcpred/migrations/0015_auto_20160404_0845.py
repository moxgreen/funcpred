# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 08:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('funcpred', '0014_auto_20160331_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionsearch',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='funcpred.Session'),
        ),
        migrations.AddField(
            model_name='session',
            name='datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 4, 8, 45, 20, 21787, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='session_id',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
