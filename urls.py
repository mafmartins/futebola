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
    # ex: /futebola/jogo/5/
    url(r'^jogador/(?P<jogador_id>[0-9]+)/$', views.jogador, name='jogador'),
    # ex: /futebola/jogo/5/
    url(r'^gerar/', views.gerarEquipas, name='gerarEquipas')
]