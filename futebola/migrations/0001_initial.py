# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 16:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ficha_de_jogo",
            fields=[
                ("ficha_id", models.AutoField(primary_key=True, serialize=False)),
                ("golos", models.IntegerField(default=0)),
                ("assistencias", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Jogador",
            fields=[
                ("jogador_id", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100)),
                ("idade", models.IntegerField(default=0)),
                ("clube_favorito", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Jogo",
            fields=[
                ("jogo_id", models.AutoField(primary_key=True, serialize=False)),
                ("data", models.DateField(default=datetime.date.today)),
                ("local", models.CharField(max_length=200)),
                ("resultado_a", models.IntegerField(default=0)),
                ("resultado_b", models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name="ficha_de_jogo",
            name="jogador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="futebola.Jogador"
            ),
        ),
        migrations.AddField(
            model_name="ficha_de_jogo",
            name="jogo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="futebola.Jogo"
            ),
        ),
    ]
