# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowInputMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlowInputSubstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('emission_factor', models.FloatField()),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
                ('simaPro_id', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Input',
            },
        ),
        migrations.CreateModel(
            name='FlowOutputMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlowOutputSubstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('emission_factor', models.FloatField()),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
                ('simaPro_id', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Output',
            },
        ),
        migrations.CreateModel(
            name='FlowSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Systems',
            },
        ),
        migrations.CreateModel(
            name='FlowTechnosphere',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
            ],
            options={
                'verbose_name': 'Technosphere intermediate',
            },
        ),
        migrations.CreateModel(
            name='FlowTechnosphereMembershipInput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
                ('partOfSystem', models.ForeignKey(to='flowdata.FlowSystem')),
                ('techFlow', models.ForeignKey(verbose_name=b'Input', to='flowdata.FlowTechnosphere')),
            ],
        ),
        migrations.CreateModel(
            name='FlowTechnosphereMembershipOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField()),
                ('note', models.CharField(max_length=500, null=True)),
                ('partOfSystem', models.ForeignKey(to='flowdata.FlowSystem')),
                ('techFlow', models.ForeignKey(verbose_name=b'Output/Emissions', to='flowdata.FlowTechnosphere')),
            ],
        ),
        migrations.CreateModel(
            name='FlowTransformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('unit', models.CharField(default=b'kg', max_length=5, choices=[(b'Mass', ((b'kg', b'kg'), (b't', b'tonne'))), (b'Energy', ((b'kWh', b'kWh'),)), (b'Volume', ((b'm3', b'm3'),)), (b'Radioactivity', ((b'Bq', b'Bq'),)), (b'Time', ((b'h', b'hours'), (b'd', b'days'))), (b'Amount', ((b'p', b'Item'),))])),
                ('category', models.CharField(default=b'Uncategorized', max_length=50)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('inputflows', models.ManyToManyField(to='flowdata.FlowInputSubstance', through='flowdata.FlowInputMembership')),
                ('outputflows', models.ManyToManyField(to='flowdata.FlowOutputSubstance', through='flowdata.FlowOutputMembership')),
                ('technosphereInputs', models.ManyToManyField(related_name='techInputs', through='flowdata.FlowTechnosphereMembershipInput', to='flowdata.FlowTechnosphere')),
                ('technosphereOutputs', models.ManyToManyField(related_name='techOutputs', through='flowdata.FlowTechnosphereMembershipOutput', to='flowdata.FlowTechnosphere')),
            ],
            options={
                'verbose_name_plural': 'Transformation processes',
            },
        ),
        migrations.AddField(
            model_name='flowtechnospheremembershipoutput',
            name='transformation',
            field=models.ForeignKey(to='flowdata.FlowTransformation'),
        ),
        migrations.AddField(
            model_name='flowtechnospheremembershipinput',
            name='transformation',
            field=models.ForeignKey(to='flowdata.FlowTransformation'),
        ),
        migrations.AddField(
            model_name='flowoutputmembership',
            name='outputsubstance',
            field=models.ForeignKey(verbose_name=b'Output/Emissions', to='flowdata.FlowOutputSubstance'),
        ),
        migrations.AddField(
            model_name='flowoutputmembership',
            name='partOfSystem',
            field=models.ForeignKey(to='flowdata.FlowSystem'),
        ),
        migrations.AddField(
            model_name='flowoutputmembership',
            name='transformation',
            field=models.ForeignKey(to='flowdata.FlowTransformation'),
        ),
        migrations.AddField(
            model_name='flowinputmembership',
            name='inputsubstance',
            field=models.ForeignKey(verbose_name=b'Input', to='flowdata.FlowInputSubstance'),
        ),
        migrations.AddField(
            model_name='flowinputmembership',
            name='partOfSystem',
            field=models.ForeignKey(to='flowdata.FlowSystem'),
        ),
        migrations.AddField(
            model_name='flowinputmembership',
            name='transformation',
            field=models.ForeignKey(to='flowdata.FlowTransformation'),
        ),
    ]
