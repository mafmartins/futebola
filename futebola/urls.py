from django.urls import re_path

from . import views

app_name = "futebola"

urlpatterns = [
    # ex: /futebola/
    re_path(r"^$", views.index, name="index"),
    # ex: /futebola/5
    re_path(r"^(?P<epoca_num>[0-9]+)/$", views.index, name="index"),
    # ex: /futebola/jogo/5/
    re_path(r"^jogo/(?P<jogo_id>[0-9]+)/$", views.jogo, name="jogo"),
    # ex: /futebola/jogador/
    re_path(r"^jogador/$", views.jogador, name="jogador"),
    # ex: /futebola/jogador/5/
    re_path(r"^jogador/(?P<jogador_id>[0-9]+)/$", views.jogador, name="jogador"),
    # ex: /futebola/regras/
    re_path(r"^regras/$", views.regras, name="regras"),
    # ex: /futebola/regras/5/
    re_path(r"^regras/(?P<epoca_num>[0-9]+)/$", views.regras, name="regras"),
    # ex: /futebola/tops/
    re_path(r"^tops/$", views.tops, name="tops"),
    # ex: /futebola/tops/5/
    re_path(r"^tops/(?P<epoca_num>[0-9]+)/$", views.tops, name="tops"),
    # ex: /futebola/gerar/
    re_path(r"^gerar/", views.gerarEquipas, name="gerarEquipas"),
    # ex: /futebola/criar-equipas/
    re_path(r"^criar-equipas/", views.criarEquipas, name="criarEquipas"),
    # ex: /futebola/numepoca/
    re_path(r"^numepoca/$", views.numerosEpoca, name="numerosEpoca"),
    # ex: /futebola/numepoca/5/
    re_path(
        r"^numepoca/(?P<epoca_num>[0-9]+)/$", views.numerosEpoca, name="numerosEpoca"
    ),
    # ex: /futebola/penalizacoes/
    re_path(r"^penalizacoes/$", views.penalizacoes, name="penalizacoes"),
    # ex: /futebola/penalizacoes/5/
    re_path(
        r"^penalizacoes/(?P<epoca_num>[0-9]+)/$",
        views.penalizacoes,
        name="penalizacoes",
    ),
]
