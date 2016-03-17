# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0008_auto_20160310_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 19, 57, 40, 738000, tzinfo=utc), verbose_name=b'timestamp'),
        ),
    ]
