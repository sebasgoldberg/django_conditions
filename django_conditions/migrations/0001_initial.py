# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 01:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionForTesting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(default=datetime.date.today, verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(default=datetime.date(9999, 12, 31), verbose_name='Fecha de fin')),
                ('value', models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Valor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelForTesting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='conditionfortesting',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_conditions.ModelForTesting'),
        ),
    ]