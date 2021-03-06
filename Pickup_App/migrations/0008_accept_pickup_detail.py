# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-26 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pickup_App', '0007_pickup_schedule_detail_flag_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accept_Pickup_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('fk_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pickup_App.Group_Detail')),
                ('fk_pick_sched', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pickup_App.Pickup_Schedule_Detail')),
                ('fk_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pickup_App.User_Detail')),
            ],
            options={
                'verbose_name_plural': 'Accept_Pickup_Detail',
                'verbose_name': 'Accept_Pickup_Detail',
            },
        ),
    ]
