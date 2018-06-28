# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Jogador(models.Model):
    jogador_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    data_nascimento = models.DateField(default=datetime.date.today)
    clube_favorito = models.CharField(max_length=100)
    guarda_redes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    defesa = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    ataque = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    velocidade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    resistencia = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    forca = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tecnica = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    passe = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    remates_longe = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    finalizacao = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    posicionamento = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    garra = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    experiencia = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    def __str__(self):
        return u"%s" % self.nome
    
    def idade(self):
        today = datetime.date.today()
        idade = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        
        return idade
      
    def nota(self):
        nota = self.guarda_redes + self.defesa + self.ataque + self.velocidade + self.resistencia + self.forca + self.tecnica + self.passe + self.remates_longe + self.finalizacao + self.posicionamento + self.garra + self.experiencia
        
        return nota
    
    def jogos(self, epoca):
        fichas = Ficha_de_jogo.objects.select_related('jogo').filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        jogs = 0
        
        for ficha in fichas:
            if not(datetime.datetime.combine(ficha.jogo.data, datetime.time(22, 0)) > datetime.datetime.today()):
                jogs += 1
                
        return jogs
    
    def vitorias(self, epoca):
        vits = 0
        
        fichas = Ficha_de_jogo.objects.select_related('jogo').filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        
        for ficha in fichas:
            if not(datetime.datetime.combine(ficha.jogo.data, datetime.time(22, 0)) > datetime.datetime.today()):
                if ficha.equipa == 'Equipa_A':
                    if ficha.jogo.resultado_a > ficha.jogo.resultado_b:
                        vits += 1
                elif ficha.equipa == 'Equipa_B':
                    if ficha.jogo.resultado_b > ficha.jogo.resultado_a:
                        vits += 1
            
        return vits
    
    def empates(self, epoca):
        emps = 0
        
        fichas = Ficha_de_jogo.objects.select_related('jogo').filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        
        for ficha in fichas:
            if not(datetime.datetime.combine(ficha.jogo.data, datetime.time(22, 0)) > datetime.datetime.today()):
                if ficha.jogo.resultado_a == ficha.jogo.resultado_b:
                    emps += 1
            
        return emps
    
    def derrotas(self, epoca):
        ders = 0
        
        fichas = Ficha_de_jogo.objects.select_related('jogo').filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        
        for ficha in fichas:
            if not(datetime.datetime.combine(ficha.jogo.data, datetime.time(22, 0)) > datetime.datetime.today()):
                if ficha.equipa == 'Equipa_A':
                    if ficha.jogo.resultado_a < ficha.jogo.resultado_b:
                        ders += 1
                elif ficha.equipa == 'Equipa_B':
                    if ficha.jogo.resultado_b < ficha.jogo.resultado_a:
                        ders += 1
            
        return ders
    
    def golos(self, epoca):
        golos = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        
        for ficha in fichas:
            golos += ficha.golos
            
        return golos
    
    def assistencias(self, epoca):
        asts = 0
        
        fichas = Ficha_de_jogo.objects.filter(jogador=self, jogo__epoca__numeracao_epoca=epoca)
        
        for ficha in fichas:
            asts += ficha.assistencias
            
        return asts
        
    
    def pontuacao(self, epoca_num):
        pontos = 0
        
        fichas = Ficha_de_jogo.objects.select_related('jogo').filter(jogador=self, jogo__epoca__numeracao_epoca=epoca_num)
        epoca = Epoca.objects.filter(numeracao_epoca=epoca_num).first()
        
        for ficha in fichas:
            if not(datetime.datetime.combine(ficha.jogo.data, datetime.time(22, 0)) > datetime.datetime.today()):
                pontos += (ficha.golos * epoca.valor_golos) + (ficha.assistencias * epoca.valor_assistencias) + epoca.valor_participacao

                if ficha.equipa == 'Equipa_A':
                    if ficha.jogo.resultado_a > ficha.jogo.resultado_b:
                        pontos += epoca.valor_vitoria
                    elif ficha.jogo.resultado_a == ficha.jogo.resultado_b:
                        pontos += epoca.valor_empate
                elif ficha.equipa == 'Equipa_B':
                    if ficha.jogo.resultado_b > ficha.jogo.resultado_a:
                        pontos += epoca.valor_vitoria
                    elif ficha.jogo.resultado_a == ficha.jogo.resultado_b:
                        pontos += epoca.valor_empate
            
        
        return pontos

    @staticmethod
    def media_idades():      
        jogadores = Jogador.objects.filter()
        soma = 0
        count = 0
        media = 0
        
        for jogador in jogadores:
            soma += jogador.idade()
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

@python_2_unicode_compatible
class Jogo(models.Model):
    jogo_id = models.AutoField(primary_key=True)
    data = models.DateField(default=datetime.date.today)
    local = models.CharField(max_length=200)
    resultado_a = models.IntegerField(default=0)
    resultado_b = models.IntegerField(default=0)
    epoca = models.ForeignKey('Epoca', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
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
                
        if len(lista_equipa_a) > len(lista_equipa_b):
            count = 0
            while (count<len(lista_equipa_a) - len(lista_equipa_b)):
                lista_equipa_b.append(Ficha_de_jogo())
        else:
            count = 0
            while (count<len(lista_equipa_b) - len(lista_equipa_a)):
                lista_equipa_a.append(Ficha_de_jogo())
                
        for f, b in zip(lista_equipa_a, lista_equipa_b):
            lista_jogo.append([f, b])
        
        return lista_jogo
    
    @staticmethod
    def media_golos_jogo(epoca):      
        jogos = Jogo.objects.filter(epoca__numeracao_epoca=epoca)
        soma = 0
        count = 0
        media = 0
        
        for jogo in jogos:
            soma += jogo.resultado_a + jogo.resultado_b
            count+=1
            
        if count != 0:
            media = soma / float(count)
        else:
            media = 0
        
        return float("{0:.2f}".format(media))

@python_2_unicode_compatible
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
    
    @property
    def epoca(self):
        return self.jogo.epoca
    
    def __str__(self):
        return u"%s | %s" % (self.jogador, self.jogo)

@python_2_unicode_compatible      
class Epoca(models.Model):
    epoca_id = models.AutoField(primary_key=True)
    numeracao_epoca = models.IntegerField(unique=True, default=0)
    inicio = models.DateField(default=datetime.date.today)
    fim = models.DateField(default=datetime.date.today)
    valor_participacao = models.IntegerField(default=0)
    valor_vitoria = models.IntegerField(default=0)
    valor_empate = models.IntegerField(default=0)
    valor_golos = models.IntegerField(default=0)
    valor_assistencias = models.IntegerField(default=0)
    
    def __str__(self):
        return u"Época %s - %s" % (self.numeracao_epoca, self.inicio.year)

    def lista_jogs(self, order_by):
        cursor = connection.cursor()
        cursor.execute('SELECT *, vitorias*'+str(self.valor_vitoria)+' + empates*'+str(self.valor_empate)+' + jogos*'+str(self.valor_participacao)+' + golos*'+str(self.valor_golos)+' + assistencias*'+str(self.valor_assistencias)+' AS pontuacao FROM ( SELECT `futebola_jogador`.`nome`, `futebola_jogador`.`jogador_id`, SUM(( CASE WHEN equipa = "equipa_a" AND resultado_a > resultado_b THEN 1 WHEN equipa = "equipa_b" AND resultado_b > resultado_a THEN 1 ELSE 0 END )) AS vitorias, SUM(( CASE WHEN equipa = "equipa_a" AND resultado_a < resultado_b THEN 1 WHEN equipa = "equipa_b" AND resultado_b < resultado_a THEN 1 ELSE 0 END )) AS derrotas, SUM(( CASE WHEN resultado_a = resultado_b THEN 1 ELSE 0 END )) AS empates, SUM(golos) AS golos, SUM(assistencias) AS assistencias, COUNT(ficha_id) AS jogos FROM `futebola_ficha_de_jogo` INNER JOIN `futebola_jogo` ON (`futebola_ficha_de_jogo`.`jogo_id` = `futebola_jogo`.`jogo_id`) INNER JOIN `futebola_epoca` ON (`futebola_jogo`.`epoca_id` = `futebola_epoca`.`epoca_id`) INNER JOIN `futebola_jogador` ON (`futebola_ficha_de_jogo`.`jogador_id` = `futebola_jogador`.`jogador_id`) WHERE ( `futebola_epoca`.`numeracao_epoca` = '+str(self.numeracao_epoca)+' AND now() > date_add(data, INTERVAL 22 HOUR) ) GROUP BY `futebola_jogador`.`nome`,`futebola_jogador`.`jogador_id` ) AS jogadores ORDER BY '+order_by)
        lista = self.dictfetchall(cursor)
            
        return lista

    def media_golos_jogador(self):      
        jogadores = self.lista_jogs('-jogos')
        total_jogos = jogadores[0]['jogos']
        soma = 0
        media = 0
        jogador_final = 0

        for jog in jogadores:
            soma = 0
            n_media = 0
            if jog['jogos'] >= 5:
                n_media = jog['golos'] / jog['jogos']
                if n_media > media:
                    media = n_media
                    jogador_final = jog

        dict = {
            "nome" : jogador_final['nome'],
            "valor" : float("{0:.2f}".format(media))
        }
        
        return dict
    
    def media_assist_jogador(self):      
        jogadores = self.lista_jogs('-jogos')
        soma = 0
        media = 0
        jogador_final = 0

        for jog in jogadores:
            soma = 0
            n_media = 0
            if jog['jogos'] >= 5:
                n_media = jog['assistencias'] / jog['jogos']
                if n_media > media:
                    media = n_media
                    jogador_final = jog

        dict = {
            "nome" : jogador_final['nome'],
            "valor" : float("{0:.2f}".format(media))
        }
        
        return dict

    def percentVitorias(self):
        jogadores = self.lista_jogs('-jogos')
        total_jogos = jogadores[0]['jogos']
        soma = 0
        percent = 0
        jogador_final = 0

        for jog in jogadores:
            if int(jog['jogos'])>total_jogos/2:
                n_percent = (jog['vitorias'] * 100) / jog['jogos']
                if n_percent > percent:
                    percent = n_percent
                    jogador_final = jog

        dict = {
            "nome" : jogador_final['nome'],
            "valor" : float("{0:.2f}".format(percent))
        }
        
        return dict

    def percentDerrotas(self):
        jogadores = self.lista_jogs('-jogos')
        total_jogos = jogadores[0]['jogos']
        soma = 0
        percent = 0
        jogador_final = 0

        for jog in jogadores:
            if int(jog['jogos'])>total_jogos/2:
                n_percent = (jog['derrotas'] * 100) / jog['jogos']
                if n_percent > percent:
                    percent = n_percent
                    jogador_final = jog

        dict = {
            "nome" : jogador_final['nome'],
            "valor" : float("{0:.2f}".format(percent))
        }
        
        return dict

    def vitoriasConsec(self):
        jogadores = self.lista_jogs('-jogos')
        cursor = connection.cursor()
        jogador_final = 0
        soma_f = 0

        for jog in jogadores:
        
            cursor.execute('SELECT CASE WHEN equipa = "equipa_a" AND resultado_a > resultado_b THEN 1 WHEN equipa = "equipa_b" AND resultado_b > resultado_a THEN 1 ELSE 0 END AS vitoria FROM `futebola_ficha_de_jogo` INNER JOIN `futebola_jogo` ON (`futebola_ficha_de_jogo`.`jogo_id` = `futebola_jogo`.`jogo_id`) INNER JOIN `futebola_epoca` ON (`futebola_jogo`.`epoca_id` = `futebola_epoca`.`epoca_id`) INNER JOIN `futebola_jogador` ON (`futebola_ficha_de_jogo`.`jogador_id` = `futebola_jogador`.`jogador_id`) WHERE (`futebola_ficha_de_jogo`.`jogador_id` = '+str(jog['jogador_id'])+' AND `futebola_epoca`.`numeracao_epoca` = '+str(self.numeracao_epoca)+')')
            
            jogos = self.dictfetchall(cursor)
            soma_t = 0
            soma_a = 0
            for jogo in jogos:
                if jogo['vitoria']>0:
                    soma_a += 1
                else:
                    if soma_a > soma_t:
                        soma_t = soma_a
                    soma_a = 0
            if soma_t > soma_f:
                soma_f = soma_t
                jogador_final = jog

        dict = {
            "nome" : jogador_final['nome'],
            "valor" : soma_f
        }
        
        return dict


    @staticmethod
    def dictfetchall(cursor): 
        "Returns all rows from a cursor as a dict" 
        desc = cursor.description 
        return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
        ]


