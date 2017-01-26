# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 05:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SportsLover', '0003_auto_20161120_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsLover.Place')),
            ],
        ),
    ]
