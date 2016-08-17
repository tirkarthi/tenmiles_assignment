# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billcalc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(verbose_name='user', null=True, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
