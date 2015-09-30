# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalmessage',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='internalmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 39, 23, 676000, tzinfo=utc), verbose_name=b'timestamp'),
        ),
    ]
