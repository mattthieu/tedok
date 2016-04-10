# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choicapp', '0006_auto_20160410_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_voted',
            name='points_given',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='item_voted',
            unique_together=set([('item', 'voter')]),
        ),
    ]