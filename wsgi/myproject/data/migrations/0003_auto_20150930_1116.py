# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20150929_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputsubstance',
            name='unit',
            field=models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))]),
        ),
        migrations.AlterField(
            model_name='outputsubstance',
            name='unit',
            field=models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))]),
        ),
        migrations.AlterField(
            model_name='process',
            name='unit',
            field=models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))]),
        ),
        migrations.AlterField(
            model_name='subprocess',
            name='unit',
            field=models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))]),
        ),
    ]
