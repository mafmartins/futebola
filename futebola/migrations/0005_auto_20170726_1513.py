# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("futebola", "0004_auto_20170726_1502"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ficha_de_jogo",
            name="equipa",
            field=models.CharField(
                choices=[("Equipa A", "Equipa A"), ("Equipa B", "Equipa B")],
                max_length=50,
            ),
        ),
    ]
