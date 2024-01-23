# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-01-21 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('code', models.CharField(max_length=50, verbose_name='Code')),
                ('track_item', models.BooleanField(default=True, verbose_name='Track Item')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Abstract Product',
                'verbose_name_plural': 'Abstract Products',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=50, null=True, unique=True, verbose_name='Code')),
                ('template_name', models.CharField(max_length=255, verbose_name='Template Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Chart',
                'verbose_name_plural': 'Charts',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code')),
                ('type_level', models.IntegerField(choices=[(1, 1), (2, 2)], default=1, verbose_name='Type Level')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('charts', models.ManyToManyField(blank=True, to='configs.Chart', verbose_name='Chart')),
            ],
            options={
                'verbose_name': 'Config',
                'verbose_name_plural': 'Configs',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('alias', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alias')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('configs', models.ManyToManyField(to='configs.Config', verbose_name='Config')),
            ],
            options={
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.AddField(
            model_name='source',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.Type', verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='abstractproduct',
            name='config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.Config', verbose_name='Config'),
        ),
        migrations.AddField(
            model_name='abstractproduct',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.AbstractProduct', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='abstractproduct',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.Type', verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='abstractproduct',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configs.Unit', verbose_name='Unit'),
        ),
    ]