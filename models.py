# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
import datetime

class Jogador(models.Model):
    jogador_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    clube_favorito = models.CharField(max_length=100)
    
    def __unicode__(self):
        return u"%s" % self.nome
    
    def jogos(self):
        fichas = Ficha_de_jogo.objects.filter(jogador=self)
        
        return len(fichas)
    
    def vitorias(self):
        vits = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self)
        
        for ficha in fichas:
            if ficha.equipa == 'Equipa_A':
                if ficha.jogo.resultado_a > ficha.jogo.resultado_b:
                    vits += 1
            elif ficha.equipa == 'Equipa_B':
                if ficha.jogo.resultado_b > ficha.jogo.resultado_a:
                    vits += 1
            
        return vits
    
    def golos(self):
        golos = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self)
        
        for ficha in fichas:
            golos += ficha.golos
            
        return golos
    
    def assistencias(self):
        asts = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self)
        
        for ficha in fichas:
            asts += ficha.assistencias
            
        return asts
        
    
    def pontuacao(self):      
        pontos = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self)
        
        for ficha in fichas:
            pontos += (ficha.golos * 10) + (ficha.assistencias * 5) + 50
            
            if ficha.equipa == 'Equipa_A':
                if ficha.jogo.resultado_a > ficha.jogo.resultado_b:
                    pontos += 100
            elif ficha.equipa == 'Equipa_B':
                if ficha.jogo.resultado_b > ficha.jogo.resultado_a:
                    pontos += 100
        
        return pontos
    
    @staticmethod
    def media_idades():      
        jogadores = Jogador.objects.filter()
        soma = 0
        count = 0
        media = 0
        
        for jogador in jogadores:
            soma += jogador.idade
            count+=1
            
        media = soma / float(count)
        
        return float("{0:.2f}".format(media))
    
    @staticmethod
    def lista_clubes():
        
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT clube_favorito FROM `futebola_jogador`')
        clubes = cursor.fetchall()
        
        count_clubes = []
        
        for clube in clubes:
            cursor.execute('SELECT COUNT(clube_favorito) FROM `futebola_jogador` WHERE clube_favorito=\"%s\"' % clube)
            count = cursor.fetchone()
            count_clubes.append({str(clube[0]) : int(count[0])})
            
        return count_clubes
    
    @staticmethod
    def media_golos_jogador():      
        jogos = Jogo.objects.filter()
        jogadores = Jogador.objects.filter()
        soma = 0
        media = 0
        
        for jogo in jogos:
            soma += jogo.resultado_a + jogo.resultado_b
            
        media = soma / float(len(jogadores))
        
        return float("{0:.2f}".format(media))
    
    @staticmethod
    def media_assist_jogador():      
        fichas = Ficha_de_jogo.objects.filter()
        jogadores = Jogador.objects.filter()
        soma = 0
        media = 0
        
        for ficha in fichas:
            soma += ficha.assistencias + ficha.assistencias
            
        media = soma / float(len(jogadores))
        
        return float("{0:.2f}".format(media))

class Jogo(models.Model):
    jogo_id = models.AutoField(primary_key=True)
    data = models.DateField(default=datetime.date.today)
    local = models.CharField(max_length=200)
    resultado_a = models.IntegerField(default=0)
    resultado_b = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"%s | %s" % (self.local, self.data)
    
    def lista_equipa(self):
        
        fichas = Ficha_de_jogo.objects.filter(jogo=self)
        
        lista_equipa_a = []
        lista_equipa_b = []
        
        lista_jogo = []
        
        for ficha in fichas:
            if ficha.equipa=='Equipa_A':
                lista_equipa_a.append(ficha)
            elif ficha.equipa=='Equipa_B': 
                lista_equipa_b.append(ficha)
                
        for f, b in zip(lista_equipa_a, lista_equipa_b):
            lista_jogo.append([f, b])
        
        return lista_jogo
    
    @staticmethod
    def media_golos_jogo():      
        jogos = Jogo.objects.filter()
        soma = 0
        count = 0
        media = 0
        
        for jogo in jogos:
            soma += jogo.resultado_a + jogo.resultado_b
            count+=1
            
        media = soma / float(count)
        
        return float("{0:.2f}".format(media))

class Ficha_de_jogo(models.Model):
    ficha_id = models.AutoField(primary_key=True)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    golos = models.IntegerField(default=0)
    assistencias = models.IntegerField(default=0)
    equipaA = 'Equipa_A'
    equipaB = 'Equipa_B'
    equipas = (
        (equipaA, 'Equipa A'),
        (equipaB, 'Equipa B')
    )
    equipa = models.CharField(max_length=50, choices=equipas)
    
    def __unicode__(self):
        return u"%s | %s" % (self.jogador, self.jogo)
