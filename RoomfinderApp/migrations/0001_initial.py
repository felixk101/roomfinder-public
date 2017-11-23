# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 22:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', models.CharField(choices=[('brunnenlech', 'Campus am Brunnenlech'), ('rotes_tor', 'Campus am Roten Tor')], default='rotes_tor', max_length=100)),
                ('name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('subject', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('long_name', models.CharField(max_length=200)),
                ('floor', models.IntegerField()),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomfinderApp.Building')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomfinderApp.Room'),
        ),
    ]