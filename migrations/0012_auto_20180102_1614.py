# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-02 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futebola', '0011_auto_20180102_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='epoca',
            name='valor_assistencias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='epoca',
            name='valor_empate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='epoca',
            name='valor_golos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='epoca',
            name='valor_participacao',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='epoca',
            name='valor_vitoria',
            field=models.IntegerField(default=0),
        ),
    ]
