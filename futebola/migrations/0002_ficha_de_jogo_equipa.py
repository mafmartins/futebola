# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("futebola", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ficha_de_jogo",
            name="equipa",
            field=models.CharField(
                choices=[("Equipa A", "Equipa A"), ("Equipa A", "Equipa B")],
                default="Equipa A",
                max_length=10,
            ),
        ),
    ]
