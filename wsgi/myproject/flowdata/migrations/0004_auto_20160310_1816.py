# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowdata', '0003_auto_20151201_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowinputmembership',
            name='uuid',
            field=models.CharField(default=b'0516d1a9-0e41-46fc-aa66-bba51e17482b', max_length=36),
        ),
        migrations.AddField(
            model_name='flowoutputmembership',
            name='uuid',
            field=models.CharField(default=b'b66effc7-6811-4ef1-8f8b-cf5de944c30a', max_length=36),
        ),
        migrations.AddField(
            model_name='flowtechnospheremembershipinput',
            name='uuid',
            field=models.CharField(default=b'1dd21e24-f263-4a0e-997e-0a1cca0b0a68', max_length=36),
        ),
        migrations.AddField(
            model_name='flowtechnospheremembershipoutput',
            name='uuid',
            field=models.CharField(default=b'226d941b-12e0-4ae9-afbc-6d9272477874', max_length=36),
        ),
        migrations.AddField(
            model_name='flowtransformation',
            name='uuid',
            field=models.CharField(default=b'9394faba-504b-443f-8922-8b271e312ef4', max_length=36),
        ),
    ]
