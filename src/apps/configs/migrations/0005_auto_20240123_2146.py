# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-01-23 13:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0004_auto_20240123_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festivalname',
            name='lunar_day',
            field=models.CharField(default='01', max_length=2, validators=[django.core.validators.MinValueValidator(1, message='LunarDay must be between 1 and 31'), django.core.validators.MaxValueValidator(31, message='LunarDay must be between 1 and 31')], verbose_name='Lunar Day'),
        ),
        migrations.AlterField(
            model_name='festivalname',
            name='lunar_month',
            field=models.CharField(default='01', max_length=2, validators=[django.core.validators.MinValueValidator(1, message='LunarMonth must be between 1 and 12'), django.core.validators.MaxValueValidator(12, message='LunarMonth must be between 1 and 12')], verbose_name='Lunar Month'),
        ),
    ]