# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowtransformation',
            name='partOfSystem',
            field=models.ForeignKey(to='flowdata.FlowSystem', null=True),
        ),
    ]
