# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Jogador, Jogo, Ficha_de_jogo
import datetime, json

def index(request):
    lista_jogadores = Jogador.objects.order_by('nome')
    
    old_lista_jogos = Jogo.objects.order_by('-data')[:5]
    lista_jogos = []
    for jogo in old_lista_jogos:
        if jogo.data < datetime.date.today():
            lista_jogos.append(jogo)
            
    lista_prox_jogos = []
    for jogo in old_lista_jogos:
        if jogo.data >= datetime.date.today():
            lista_prox_jogos.append(jogo)
    
    lista_clubes = []
    for item in Jogador.lista_clubes():
        for k, v in item.iteritems():
            lista_clubes.append([k,v])
    
    unsorted_results = lista_jogadores.all()
    lista_jogadores = sorted(unsorted_results, key= lambda t: t.pontuacao(), reverse=True)
    lista_jog_mais_reg = sorted(unsorted_results, key= lambda t: t.jogos(), reverse=True)[:5]
    
    media_idades = Jogador.media_idades()
    media_golos_jogo = Jogo.media_golos_jogo()
    media_golos_jogador = Jogador.media_golos_jogador()
    media_assist_jogador = Jogador.media_assist_jogador()
    
    context = {
        'lista_jogadores': lista_jogadores,
        'lista_jog_mais_reg': lista_jog_mais_reg,
        'lista_jogos': lista_jogos,
        'lista_prox_jogos': lista_prox_jogos,
        'lista_clubes': lista_clubes,
        'media_idades' : media_idades,
        'media_golos_jogo' : media_golos_jogo,
        'media_golos_jogador' : media_golos_jogador,
        'media_assist_jogador' : media_assist_jogador
    }
    return render(request, 'futebola/index.html', context)

def jogo(request, jogo_id):
    jogo = get_object_or_404(Jogo, jogo_id=jogo_id)
    
    lista_equipa = jogo.lista_equipa
    
    context = {
        'jogo' : jogo,
        'lista_equipa' : lista_equipa
    }
        
    return render(request, 'futebola/jogo.html', context)

def jogador(request, jogador_id):
    jogador = get_object_or_404(Jogador, jogador_id=jogador_id)
    
    context = {
        'jogador' : jogador
    }
        
    return render(request, 'futebola/jogador.html', context)