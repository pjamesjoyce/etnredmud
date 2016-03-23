# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0007_auto_20160317_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowinputmembership',
            name='uuid',
            field=models.CharField(default=b' ', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowoutputmembership',
            name='uuid',
            field=models.CharField(default=b' ', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipinput',
            name='uuid',
            field=models.CharField(default=b' ', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipoutput',
            name='uuid',
            field=models.CharField(default=b' ', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtransformation',
            name='uuid',
            field=models.CharField(default=b' ', max_length=36),
        ),
    ]
