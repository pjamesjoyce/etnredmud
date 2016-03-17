# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0005_auto_20160310_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowinputmembership',
            name='uuid',
            field=models.CharField(default=b'51545967-3cd4-47c3-8638-ce0c36fa3e73', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowoutputmembership',
            name='uuid',
            field=models.CharField(default=b'f2ae8007-db34-4fe2-810f-66a7697b3afe', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipinput',
            name='uuid',
            field=models.CharField(default=b'ec4a9330-3fc3-4c76-a77b-63ee5257c3c4', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtechnospheremembershipoutput',
            name='uuid',
            field=models.CharField(default=b'2de4a068-6348-4171-9102-1d76750a6e01', max_length=36),
        ),
        migrations.AlterField(
            model_name='flowtransformation',
            name='uuid',
            field=models.CharField(default=b'6d20f7d1-e679-4776-9807-a6d941c2316f', max_length=36),
        ),
    ]
