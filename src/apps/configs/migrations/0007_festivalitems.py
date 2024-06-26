# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-01-23 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0006_auto_20240123_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('enable', models.BooleanField(default=True, verbose_name='Enabled')),
                ('order_sn', models.IntegerField(default=9, verbose_name='Order SN')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('festival_name', models.ManyToManyField(to='configs.FestivalName', verbose_name='Festival Name')),
                ('product_id', models.ManyToManyField(to='configs.AbstractProduct', verbose_name='Product ID')),
                ('source', models.ManyToManyField(to='configs.Source', verbose_name='Source')),
            ],
            options={
                'verbose_name': 'Festal Item',
                'ordering': ('order_sn',),
            },
        ),
    ]
