# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-05-06 09:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configs', '0009_auto_20240123_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.today, verbose_name='Date')),
                ('file_id', models.CharField(max_length=120, unique=True, verbose_name='File ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Daily Report',
                'verbose_name_plural': 'Daily Reports',
            },
        ),
        migrations.CreateModel(
            name='DailyTran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_price', models.FloatField(blank=True, null=True, verbose_name='Up Price')),
                ('mid_price', models.FloatField(blank=True, null=True, verbose_name='Mid Price')),
                ('low_price', models.FloatField(blank=True, null=True, verbose_name='Low Pirce')),
                ('avg_price', models.FloatField(verbose_name='Average Price')),
                ('avg_weight', models.FloatField(blank=True, null=True, verbose_name='Average Weight')),
                ('volume', models.FloatField(blank=True, null=True, verbose_name='Volume')),
                ('date', models.DateField(default=datetime.datetime.today, verbose_name='Date')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('not_updated', models.IntegerField(default=0, verbose_name='Not Updated Count')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configs.AbstractProduct', verbose_name='Product')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configs.Source', verbose_name='Source')),
            ],
            options={
                'verbose_name': 'Daily Transition',
                'verbose_name_plural': 'Daily Transitions',
            },
        ),
        migrations.CreateModel(
            name='FestivalReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=120, unique=True, verbose_name='File ID')),
                ('file_volume_id', models.CharField(blank=True, max_length=120, null=True, verbose_name='File Volume ID')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('festival_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configs.Festival', verbose_name='Festival ID')),
            ],
            options={
                'verbose_name': 'Festival Report',
                'verbose_name_plural': 'Festival Reports',
            },
        ),
    ]
