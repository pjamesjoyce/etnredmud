# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0011_auto_20160317_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 22, 10, 0, 54, 374000, tzinfo=utc), verbose_name=b'timestamp'),
        ),
    ]
