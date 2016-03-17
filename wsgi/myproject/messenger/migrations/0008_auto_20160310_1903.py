# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0007_auto_20160310_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 18, 3, 10, 556000, tzinfo=utc), verbose_name=b'timestamp'),
        ),
    ]
