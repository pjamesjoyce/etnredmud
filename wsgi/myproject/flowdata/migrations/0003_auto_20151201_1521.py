# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0002_flowtransformation_partofsystem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowtransformation',
            name='partOfSystem',
        ),
        migrations.AddField(
            model_name='flowtransformation',
            name='partOfSystem',
            field=models.ManyToManyField(to='flowdata.FlowSystem'),
        ),
    ]
