# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import importData.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data_file', models.FileField(upload_to=importData.models.get_upload_file_name, blank=True)),
            ],
        ),
    ]
