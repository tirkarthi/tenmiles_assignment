# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('company_info', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', serialize=False, auto_created=True)),
                ('start_date', models.DateField()),
                ('cost_per_hour', models.FloatField()),
                ('client', models.ForeignKey(to='billcalc.Client')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('time_spent', models.FloatField()),
                ('project', models.ForeignKey(to='billcalc.Project')),
            ],
        ),
    ]
