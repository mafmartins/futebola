# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import Jogador, Jogo, Ficha_de_jogo, Epoca, Penalizacao
import datetime
import json
from django.urls import reverse


def index(request, epoca_num=0):
    if not epoca_num:
        epoca_num = Epoca.objects.order_by("-epoca_id").first().numeracao_epoca
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)

    old_lista_jogos = Jogo.objects.filter(epoca__numeracao_epoca=epoca_num).order_by(
        "-data"
    )

    lista_jogos = []
    for idx, jogo in enumerate(old_lista_jogos):
        if idx > 4:
            break
        if jogo.data < datetime.date.today():
            lista_jogos.append(jogo)

    lista_prox_jogos = []
    for idx, jogo in enumerate(old_lista_jogos):
        if idx > 4:
            break
        if jogo.data >= datetime.date.today():
            lista_prox_jogos.append(jogo)

    lista_clubes = []
    for item in Jogador.lista_clubes():
        for k, v in item.items():
            lista_clubes.append([k, v])

    lista_jogadores = epoca.lista_jogs(
        "-pontuacao, -golos, -assistencias, -jogos, -vitorias, derrotas"
    )
    lista_jog_mais_reg = epoca.lista_jogs("-jogos")[:5]
    lista_jog_mais_gol = epoca.lista_jogs("-golos, jogos, -vitorias")[:5]
    lista_jog_mais_ass = epoca.lista_jogs("-assistencias, jogos, -vitorias")[:5]
    cuurl = reverse("futebola:index")
    is_home = True

    context = {
        "epocas": epocas,
        "epoca": epoca,
        "epoca_num": epoca_num,
        "lista_jogadores": lista_jogadores,
        "lista_jog_mais_reg": lista_jog_mais_reg,
        "lista_jogos": lista_jogos,
        "lista_prox_jogos": lista_prox_jogos,
        "lista_clubes": lista_clubes,
        "lista_jog_mais_gol": lista_jog_mais_gol,
        "lista_jog_mais_ass": lista_jog_mais_ass,
        "cuurl": cuurl,
        "is_home": is_home,
    }

    return render(request, "futebola/index.html", context)


def jogo(request, jogo_id):
    jogo = get_object_or_404(Jogo, jogo_id=jogo_id)

    lista_equipa = jogo.lista_equipa

    context = {
        "jogo": jogo,
        "lista_equipa": lista_equipa,
        "bonuses_list": jogo.bonuses_list,
        "penalties_list": jogo.penalties_list,
    }

    return render(request, "futebola/jogo.html", context)


def jogador(request, jogador_id):
    epoca_num = Epoca.objects.order_by("-epoca_id").first().numeracao_epoca

    jogador = get_object_or_404(Jogador, jogador_id=jogador_id)
    epocas_obj = Epoca.objects.order_by("-epoca_id")

    fichas_jogo = (
        Ficha_de_jogo.objects.select_related("jogo")
        .filter(jogador=jogador, jogo__epoca__numeracao_epoca=epoca_num)
        .order_by("-ficha_id")[:10]
    )
    lista_jogos = [ficha.jogo for ficha in fichas_jogo]

    context = {
        "epocas_obj": epocas_obj,
        "jogador": jogador,
        "lista_jogos": lista_jogos,
        "cuurl": reverse("futebola:jogador"),
    }

    return render(request, "futebola/jogador.html", context)


def numerosEpoca(
    request, epoca_num=Epoca.objects.order_by("-epoca_id").first().numeracao_epoca
):
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)

    media_golos_jogador = epoca.media_golos_jogador()
    media_assist_jogador = epoca.media_assist_jogador()
    percent_vitorias_jogador = epoca.percentVitorias()
    percent_derrotas_jogador = epoca.percentDerrotas()
    mais_jogos_jogador = epoca.lista_jogs("-jogos")[0]
    vit_consec_jogador = epoca.vitoriasConsec()[0]

    context = {
        "epocas": epocas,
        "epoca": epoca,
        "media_golos_jogador": media_golos_jogador,
        "media_assist_jogador": media_assist_jogador,
        "percent_vitorias_jogador": percent_vitorias_jogador,
        "percent_derrotas_jogador": percent_derrotas_jogador,
        "mais_jogos_jogador": mais_jogos_jogador,
        "vit_consec_jogador": vit_consec_jogador,
        "cuurl": reverse("futebola:numerosEpoca"),
    }

    return render(request, "futebola/numEpoca.html", context)


def regras(
    request, epoca_num=Epoca.objects.order_by("-epoca_id").first().numeracao_epoca
):
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)

    context = {
        "epocas": epocas,
        "epoca": epoca,
        "cuurl": reverse("futebola:regras"),
    }

    return render(request, "futebola/regras.html", context)


def tops(
    request, epoca_num=Epoca.objects.order_by("-epoca_id").first().numeracao_epoca
):
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)
    lista_jog_mais_reg = epoca.lista_jogs("-jogos")[:5]
    lista_jog_mais_gol = epoca.lista_jogs("-golos, jogos, -vitorias")[:5]
    lista_jog_mais_ass = epoca.lista_jogs("-assistencias, jogos, -vitorias")[:5]
    lista_jog_mais_vit = epoca.lista_jogs("-vitorias, jogos")[:5]
    lista_jog_mais_comb = epoca.lista_jogs("-combinado")[:5]
    lista_jog_golos_sof = epoca.media_golos_sofridos()[:5]

    for jog in lista_jog_mais_comb:
        soma = jog["golos"] + jog["assistencias"]
        jog["combinado"] = soma

    lista_jog_mais_comb = sorted(
        lista_jog_mais_comb, key=lambda k: k["combinado"], reverse=True
    )

    context = {
        "epocas": epocas,
        "epoca": epoca,
        "cuurl": reverse("futebola:tops"),
        "lista_jog_mais_gol": lista_jog_mais_gol,
        "lista_jog_mais_ass": lista_jog_mais_ass,
        "lista_jog_mais_reg": lista_jog_mais_reg,
        "lista_jog_mais_vit": lista_jog_mais_vit,
        "lista_jog_mais_comb": lista_jog_mais_comb,
        "lista_jog_golos_sof": lista_jog_golos_sof,
    }

    return render(request, "futebola/tops.html", context)


def penalizacoes(
    request, epoca_num=Epoca.objects.order_by("-epoca_id").first().numeracao_epoca
):
    epocas = Epoca.objects.all()
    epoca = get_object_or_404(Epoca, numeracao_epoca=epoca_num)
    penalizacoes = Penalizacao.objects.filter(
        epoca__numeracao_epoca=epoca_num
    ).order_by("-data")

    context = {
        "epocas": epocas,
        "epoca": epoca,
        "penalizacoes": penalizacoes,
        "cuurl": reverse("futebola:penalizacoes"),
    }

    return render(request, "futebola/penalizacoes.html", context)


def gerarEquipas(request):
    lista_jogadores = Jogador.objects.order_by("nome")
    lista_jogadores = sorted(lista_jogadores, key=lambda t: t.nota(), reverse=True)

    context = {"lista_jogadores": lista_jogadores}

    if request.method == "GET":
        return render(request, "futebola/gerarEquipas.html", context)
    else:
        ar = []
        ints = []
        post_list = request.POST.copy()
        for item in post_list:
            try:
                obj = {item: int(post_list[item])}
                ar.append(obj)
                ints.append(int(post_list[item]))
            except Exception:
                continue

        vals1, vals2 = team(ints)

        team1 = []
        team2 = []

        for x in vals1:
            for y in post_list:
                try:
                    if x == int(post_list[y]):
                        team1.append({y: post_list[y]})
                        del post_list[y]
                        break
                except Exception:
                    continue
        for x in vals2:
            for y in post_list:
                try:
                    if x == int(post_list[y]):
                        team2.append({y: post_list[y]})
                        del post_list[y]
                        break
                except Exception:
                    continue

        equipa1 = []
        equipa2 = []
        sume1 = 0
        sume2 = 0

        for x in team1:
            equipa1.append(
                get_object_or_404(Jogador, jogador_id=int(list(x.keys())[0]))
            )
            sume1 += int(list(x.values())[0])

        for x in team2:
            equipa2.append(
                get_object_or_404(Jogador, jogador_id=int(list(x.keys())[0]))
            )
            sume2 += int(list(x.values())[0])

        context = {
            "equipa1": equipa1,
            "equipa2": equipa2,
            "somae1": sume1,
            "somae2": sume2,
            "cuurl": reverse("futebola:gerarEquipas"),
        }

        # return JsonResponse(post_list, safe=False)
        return render(request, "futebola/verEquipasGeradas.html", context)


def criarEquipas(request):

    if request.method == "POST":

        data = json.loads(request.body)

        novoJogo = Jogo(
            local=data.get("local"), epoca=Epoca.objects.order_by("-epoca_id").first()
        )
        novoJogo.save()

        for jogadorId in data.get("equipaA"):
            ficha = Ficha_de_jogo(
                jogador=Jogador.objects.get(pk=jogadorId),
                equipa="Equipa_A",
                jogo=novoJogo,
            )
            ficha.save()

        for jogadorId in data.get("equipaB"):
            ficha = Ficha_de_jogo(
                jogador=Jogador.objects.get(pk=jogadorId),
                equipa="Equipa_B",
                jogo=novoJogo,
            )
            ficha.save()

        return HttpResponse(novoJogo.jogo_id)

    return HttpResponseNotFound("Método incompatível")


def team(t):
    iterations = range(2, int(len(t) / 2 + 1))

    totalscore = sum(t)
    halftotalscore = totalscore / 2.0

    oldmoves = {}

    for p in t:
        people_left = t[:]
        people_left.remove(p)
        oldmoves[p] = people_left

    if iterations == []:
        solution = min(
            map(lambda i: (abs(float(i) - halftotalscore), i), oldmoves.keys())
        )
        return (solution[1], sum(oldmoves[solution[1]]), oldmoves[solution[1]])

    for n in iterations:
        newmoves = {}
        for total, roster in oldmoves.items():
            for p in roster:
                people_left = roster[:]
                people_left.remove(p)
                newtotal = total + p
                if newtotal > halftotalscore:
                    continue
                newmoves[newtotal] = people_left
        oldmoves = newmoves

    solution = min(map(lambda i: (abs(float(i) - halftotalscore), i), oldmoves.keys()))

    for item in oldmoves[solution[1]]:
        for obj in t:
            if item == obj:
                t.remove(obj)
                break
    return (oldmoves[solution[1]], t)
