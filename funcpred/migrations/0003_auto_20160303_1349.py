# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcpred', '0002_auto_20160303_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gene',
            name='entrez',
        ),
        migrations.AddField(
            model_name='gene',
            name='biotype',
            field=models.CharField(choices=[(b'lincRNA', b'lincRNA'), (b'other', b'other'), (b'protein_coding', b'protein_coding'), (b'antisense', b'antisense'), (b'pseudogene', b'pseudogene')], default=b'other', max_length=14),
        ),
        migrations.AddField(
            model_name='gene',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gene',
            name='status',
            field=models.CharField(default='', max_length=160),
            preserve_default=False,
        ),
    ]
