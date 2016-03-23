# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0006_auto_20160310_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowinputmembership',
            name='uuid',
            field=models.CharField(default=b'c251f540-18ad-48e1-8734-ae12a9a10662', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowoutputmembership',
            name='uuid',
            field=models.CharField(default=b'8273d9e4-8ad5-446c-a4c2-803d5d0ab2e0', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipinput',
            name='uuid',
            field=models.CharField(default=b'165a5f1d-a538-464d-8951-732e0cb36aa9', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipoutput',
            name='uuid',
            field=models.CharField(default=b'd919d809-a266-4329-90b1-4e83aca54d26', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtransformation',
            name='uuid',
            field=models.CharField(default=b'84d50a87-110f-4ab8-8635-f8a882bf8db5', max_length=36),
        ),
    ]
