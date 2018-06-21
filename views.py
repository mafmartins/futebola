# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Jogador, Jogo, Ficha_de_jogo, Epoca
import datetime, json

# import the logging library
import logging
from django.db import connection

def index(request, epoca_num=Epoca.objects.order_by('-epoca_id').first().numeracao_epoca):
    #fError = open('timers.log','a')
    Tinit = datetime.datetime.now()
    #fError.write("\nInicio: "+str(datetime.datetime.now()))
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 1: "+str(Tnow))
    old_lista_jogos = Jogo.objects.filter(epoca__numeracao_epoca = epoca_num).order_by('-data')
    #logging.warning('WUT!')
    
    if(old_lista_jogos.count()>0):
        jogadores_q_jogaram = [jogador.jogador_id for jogador in Jogador.objects.all() if jogador.jogos(epoca_num) > 0]
        lista_jogadores = Jogador.objects.filter(jogador_id__in=jogadores_q_jogaram).order_by('nome')
    else:
        lista_jogadores = Jogador.objects.order_by('nome')
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 2: "+str(Tnow))
    lista_jogos = []
    for idx, jogo in enumerate(old_lista_jogos):
        if idx > 4:
            break
        if jogo.data < datetime.date.today():
            lista_jogos.append(jogo)
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 3: "+str(Tnow))        
    lista_prox_jogos = []
    for idx, jogo in enumerate(old_lista_jogos):
        if idx > 4:
            break
        if jogo.data >= datetime.date.today():
            lista_prox_jogos.append(jogo)
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 4: "+str(Tnow))
    lista_clubes = []
    for item in Jogador.lista_clubes():
        for k, v in item.items():
            lista_clubes.append([k,v])
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 5: "+str(Tnow))
    unsorted_results = lista_jogadores.all()
    lista_jogadores = sorted(unsorted_results, key= lambda t: t.pontuacao(epoca_num), reverse=True)
    lista_jog_mais_reg = sorted(unsorted_results, key= lambda t: t.jogos(epoca_num), reverse=True)[:5]
    lista_jog_mais_gol = sorted(unsorted_results, key= lambda t: t.golos(epoca_num), reverse=True)[:5]
    lista_jog_mais_ass = sorted(unsorted_results, key= lambda t: t.assistencias(epoca_num), reverse=True)[:5]
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 6: "+str(Tnow))
    media_idades = Jogador.media_idades()
    media_golos_jogo = Jogo.media_golos_jogo(epoca_num)
    media_golos_jogador = Jogador.media_golos_jogador(epoca_num)
    media_assist_jogador = Jogador.media_assist_jogador(epoca_num)
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep 7: "+str(Tnow))
    context = {
        'epocas': epocas,
        'epoca': epoca,
        'epoca_num': epoca_num,
        'lista_jogadores': lista_jogadores,
        'lista_jog_mais_reg': lista_jog_mais_reg,
        'lista_jogos': lista_jogos,
        'lista_prox_jogos': lista_prox_jogos,
        'lista_clubes': lista_clubes,
        'media_idades' : media_idades,
        'media_golos_jogo' : media_golos_jogo,
        'media_golos_jogador' : media_golos_jogador,
        'media_assist_jogador' : media_assist_jogador,
        'lista_jog_mais_gol' : lista_jog_mais_gol,
        'lista_jog_mais_ass' : lista_jog_mais_ass
    }
    Tnow = datetime.datetime.now() - Tinit
    #fError.write("\nStep Final: "+str(Tnow))
    #fError.write("\nFim: "+str(datetime.datetime.now()))
    #fError.write("\n"+str(connection.queries))
    #fError.close()
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
    epoca_num = Epoca.objects.order_by('-epoca_id').first().numeracao_epoca
    
    context = {
        'epoca_num' : epoca_num,
        'jogador' : jogador
    }
        
    return render(request, 'futebola/jogador.html', context)
  
def gerarEquipas(request):
    lista_jogadores = Jogador.objects.order_by('nome')
    lista_jogadores = sorted(lista_jogadores, key= lambda t: t.nota(), reverse=True)
    
    context = {
        'lista_jogadores': lista_jogadores
    }
    
    if request.method == 'GET':
        return render(request, 'futebola/gerarEquipas.html', context)
    else:            
        ar = []
        ints = []
        post_list = request.POST.copy()
        for item in post_list:
            try:
                obj = {item : int(post_list[item])}
                ar.append(obj)
                ints.append(int(post_list[item]))
            except:
                continue

        vals1, vals2 = team(ints)

        team1 = []
        team2 = []

        for x in vals1:
          for y in post_list:
            try:
              if x == int(post_list[y]):
                team1.append({y : post_list[y]})
                del post_list[y]
                break
            except:
              continue
        for x in vals2:
          for y in post_list:
            try:
              if x == int(post_list[y]):
                team2.append({y : post_list[y]})
                del post_list[y]
                break
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
        
        #return JsonResponse(post_list, safe=False)
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
        for total, roster in oldmoves.items():
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
