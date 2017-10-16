# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
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
  
def gerarEquipas(request):
    lista_jogadores = Jogador.objects.order_by('nome')
    
    context = {
        'lista_jogadores': lista_jogadores
    }
    
    if request.method == 'GET':
        return render(request, 'futebola/gerarEquipas.html', context)
    else:            
        ar = []
        ints = []
        for item in request.POST:
            try:
                obj = {item : int(request.POST[item])}
                ar.append(obj)
                ints.append(int(request.POST[item]))
            except:
                continue

        vals1, vals2 = team(ints)

        team1 = []
        team2 = []

        for x in vals1:
          for y in request.POST:
            try:
              if x == int(request.POST[y]):
                team1.append({y : request.POST[y]})
            except:
              continue
        for x in vals2:
          for y in request.POST:
            try:
              if x == int(request.POST[y]):
                team2.append({y : request.POST[y]})
            except:
              continue
        
        equipa1 = []
        equipa2 = []
        sume1 = 0
        sume2 = 0
        
        for x in team1:
            equipa1.append(get_object_or_404(Jogador, jogador_id=int(x.keys()[0])))
            sume1 += int(x.values()[0])
            
        for x in team2:
            equipa2.append(get_object_or_404(Jogador, jogador_id=int(x.keys()[0])))
            sume2 += int(x.values()[0])
            
        context = {
            'equipa1': equipa1,
            'equipa2': equipa2,
            'somae1' : sume1,
            'somae2' : sume2
        }
        
        return render(request, 'futebola/verEquipasGeradas.html', context)
    
def team(t):
    iterations = range(2, len(t)/2+1)

    totalscore = sum(t)
    halftotalscore = totalscore/2.0

    oldmoves = {}
    
    rest = []

    for p in t:
        people_left = t[:]
        people_left.remove(p)
        oldmoves[p] = people_left

    if iterations == []:
        solution = min(map(lambda i: (abs(float(i)-halftotalscore), i), oldmoves.keys()))
        return (solution[1], sum(oldmoves[solution[1]]), oldmoves[solution[1]])

    for n in iterations:
        newmoves = {}
        for total, roster in oldmoves.iteritems():
            for p in roster:
                people_left = roster[:]
                people_left.remove(p)
                newtotal = total+p
                if newtotal > halftotalscore: continue
                newmoves[newtotal] = people_left
        oldmoves = newmoves

    solution = min(map(lambda i: (abs(float(i)-halftotalscore), i), oldmoves.keys()))
    
    for item in oldmoves[solution[1]]:
        for obj in t:
            if item == obj:
                t.remove(obj)
                break
    #return (sum(oldmoves[solution[1]]), oldmoves[solution[1]], solution[1], t)
    return (oldmoves[solution[1]], t)
