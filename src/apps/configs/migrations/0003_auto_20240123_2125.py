# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-01-23 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0002_auto_20240121_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roc_year', models.CharField(default=113, max_length=3, verbose_name='ROC Year')),
                ('enable', models.BooleanField(default=True, verbose_name='Enabled')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Festival',
                'verbose_name_plural': 'Festivals',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='FestivalName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Name')),
                ('enable', models.BooleanField(default=True, verbose_name='Enabled')),
                ('lunar_month', models.CharField(default='01', max_length=2, verbose_name='Lunar Month')),
                ('lunar_day', models.CharField(default='01', max_length=2, verbose_name='Lunar Day')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Festival Name',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Month',
                'verbose_name_plural': 'Months',
            },
        ),
        migrations.AddField(
            model_name='festival',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.FestivalName', verbose_name='Name'),
        ),
    ]
