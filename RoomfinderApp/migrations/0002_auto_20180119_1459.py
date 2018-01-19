# Generated by Django 2.0.1 on 2018-01-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomfinderApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='course',
            field=models.CharField(default='Unbekannt', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(),
        ),
    ]