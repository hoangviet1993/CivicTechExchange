# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-11 01:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('democracylab', '0002_contributor_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTaggedTechnologies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contributor',
            name='country',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='usertaggedtechnologies',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='democracylab.Contributor'),
        ),
        migrations.AddField(
            model_name='usertaggedtechnologies',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='democracylab_usertaggedtechnologies_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user_technologies',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='democracylab.UserTaggedTechnologies', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]