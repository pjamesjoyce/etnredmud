# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messenger', '0002_auto_20150930_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internalmessage',
            name='recipient',
        ),
        migrations.AddField(
            model_name='internalmessage',
            name='recipient',
            field=models.ManyToManyField(related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='internalmessage',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 9, 58, 7, 1000, tzinfo=utc), verbose_name=b'timestamp'),
        ),
    ]
