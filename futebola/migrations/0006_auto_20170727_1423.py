# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("futebola", "0005_auto_20170726_1513"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ficha_de_jogo",
            name="equipa",
            field=models.CharField(
                choices=[("Equipa_A", "Equipa A"), ("Equipa_B", "Equipa B")],
                max_length=50,
            ),
        ),
    ]
