from django.template import Library

register = Library()


@register.filter
def jogos(jogador, epoca):
    return jogador.jogos(epoca)


@register.filter
def vitorias(jogador, epoca):
    return jogador.vitorias(epoca)


@register.filter
def empates(jogador, epoca):
    return jogador.empates(epoca)


@register.filter
def derrotas(jogador, epoca):
    return jogador.derrotas(epoca)


@register.filter
def golos(jogador, epoca):
    return jogador.golos(epoca)


@register.filter
def assistencias(jogador, epoca):
    return jogador.assistencias(epoca)


@register.filter
def pontuacao(jogador, epoca):
    return jogador.pontuacao(epoca)
