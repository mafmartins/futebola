# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-26 15:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("futebola", "0013_auto_20180105_0940"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jogador",
            name="idade",
        ),
        migrations.AddField(
            model_name="jogador",
            name="data_nascimento",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
