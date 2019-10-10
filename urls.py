from django.conf.urls import url

from . import views

app_name = 'futebola'
urlpatterns = [
    # ex: /futebola/
    url(r'^$', views.index, name='index'),
    # ex: /futebola/5
    url(r'^(?P<epoca_num>[0-9]+)/$', views.index, name='index'),
    # ex: /futebola/jogo/5/
    url(r'^jogo/(?P<jogo_id>[0-9]+)/$', views.jogo, name='jogo'),
    # ex: /futebola/jogador/
    url(r'^jogador/$', views.jogador, name='jogador'),
    # ex: /futebola/jogador/5/
    url(r'^jogador/(?P<jogador_id>[0-9]+)/$', views.jogador, name='jogador'),
    # ex: /futebola/regras/
    url(r'^regras/$', views.regras, name='regras'),
    # ex: /futebola/regras/5/
    url(r'^regras/(?P<epoca_num>[0-9]+)/$', views.regras, name='regras'),
    # ex: /futebola/tops/
    url(r'^tops/$', views.tops, name='tops'),
    # ex: /futebola/tops/5/
    url(r'^tops/(?P<epoca_num>[0-9]+)/$', views.tops, name='tops'),
    # ex: /futebola/gerar/
    url(r'^gerar/', views.gerarEquipas, name='gerarEquipas'),
    # ex: /futebola/numepoca/
    url(r'^numepoca/$', views.numerosEpoca, name='numerosEpoca'),
    # ex: /futebola/numepoca/5/
    url(r'^numepoca/(?P<epoca_num>[0-9]+)/$', views.numerosEpoca, name='numerosEpoca'),
    # ex: /futebola/penalizacoes/
    url(r'^penalizacoes/$', views.penalizacoes, name='penalizacoes'),
    # ex: /futebola/penalizacoes/5/
    url(r'^penalizacoes/(?P<epoca_num>[0-9]+)/$', views.penalizacoes, name='penalizacoes'),
]