# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Jogador, Jogo, Ficha_de_jogo, Epoca, Penalizacao, Bonus

admin.site.register(Jogador)
admin.site.register(Jogo)
admin.site.register(Ficha_de_jogo)
admin.site.register(Epoca)
admin.site.register(Penalizacao)
admin.site.register(Bonus)
