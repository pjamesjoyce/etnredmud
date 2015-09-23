# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import data.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InputMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputSubstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('emission_factor', models.FloatField()),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kwh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'bq', b'Bq'),)), (b'Time', ((b'hr', b'hours'), (b'dy', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
            ],
            options={
                'verbose_name': 'Input',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='OutputMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OutputSubstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('emission_factor', models.FloatField()),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kwh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'bq', b'Bq'),)), (b'Time', ((b'hr', b'hours'), (b'dy', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
            ],
            options={
                'verbose_name': 'Output',
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('output', models.CharField(max_length=128)),
                ('output_amount', models.FloatField()),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kwh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'bq', b'Bq'),)), (b'Time', ((b'hr', b'hours'), (b'dy', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Processes',
            },
        ),
        migrations.CreateModel(
            name='ProcessMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
                ('process', models.ForeignKey(to='data.Process')),
            ],
        ),
        migrations.CreateModel(
            name='SubProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kwh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'bq', b'Bq'),)), (b'Time', ((b'hr', b'hours'), (b'dy', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
                ('category', models.CharField(default=b'Uncategorized', max_length=50)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('inputs', models.ManyToManyField(to='data.InputSubstance', through='data.InputMembership')),
                ('outputs', models.ManyToManyField(to='data.OutputSubstance', through='data.OutputMembership')),
            ],
            options={
                'verbose_name_plural': 'Subprocesses',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('esr_number', models.IntegerField(null=True, blank=True)),
                ('work_package', models.IntegerField(null=True, blank=True)),
                ('profile_picture', models.FileField(upload_to=data.models.get_upload_file_name, blank=True)),
                ('institution', models.ForeignKey(blank=True, to='data.Institution', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='processmembership',
            name='subprocess',
            field=models.ForeignKey(to='data.SubProcess'),
        ),
        migrations.AddField(
            model_name='process',
            name='subprocesses',
            field=models.ManyToManyField(to='data.SubProcess', through='data.ProcessMembership'),
        ),
        migrations.AddField(
            model_name='outputmembership',
            name='outputsubstance',
            field=models.ForeignKey(verbose_name=b'Output/Emissions', to='data.OutputSubstance'),
        ),
        migrations.AddField(
            model_name='outputmembership',
            name='subprocess',
            field=models.ForeignKey(to='data.SubProcess'),
        ),
        migrations.AddField(
            model_name='inputmembership',
            name='inputsubstance',
            field=models.ForeignKey(verbose_name=b'Input', to='data.InputSubstance'),
        ),
        migrations.AddField(
            model_name='inputmembership',
            name='subprocess',
            field=models.ForeignKey(to='data.SubProcess'),
        ),
    ]
