# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-30 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pickup_App', '0009_auto_20200328_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_detail',
            name='token',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
