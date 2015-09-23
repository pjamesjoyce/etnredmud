# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Site content',
                'verbose_name_plural': 'Site content',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=200)),
                ('href', models.CharField(max_length=200)),
                ('alt', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='link1',
            field=models.ForeignKey(related_name='link1', blank=True, to='content.Link', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='link2',
            field=models.ForeignKey(related_name='link2', blank=True, to='content.Link', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='link3',
            field=models.ForeignKey(related_name='link3', blank=True, to='content.Link', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='link4',
            field=models.ForeignKey(related_name='link4', blank=True, to='content.Link', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='link5',
            field=models.ForeignKey(related_name='link5', blank=True, to='content.Link', null=True),
        ),
    ]
