# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0004_auto_20160310_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowinputmembership',
            name='uuid',
            field=models.CharField(default=b'76d58159-f5ec-4cef-b064-079c8e4b3d5f', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowoutputmembership',
            name='uuid',
            field=models.CharField(default=b'8f692fd0-7fae-4baa-8e1b-b044c53f7fca', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipinput',
            name='uuid',
            field=models.CharField(default=b'd7d255fc-f5d3-4453-9d35-4f42c3eb1793', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipoutput',
            name='uuid',
            field=models.CharField(default=b'ed8f4a2d-0044-48f0-bb95-c1ba453c2dd3', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtransformation',
            name='uuid',
            field=models.CharField(default=b'c1f3ffbc-27b2-4581-ad29-0dc0491d66cd', max_length=36),
        ),
    ]
