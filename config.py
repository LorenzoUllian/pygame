"""Configurações do jogo: tamanhos, física do pulo, obstáculos, planetas, cores e estados."""
from os import path

# ===== Pastas e arquivos =====
# path.dirname(__file__) é a pasta onde está este arquivo (a pasta do jogo).
# path.join junta os nomes das pastas do jeito certo para Windows, Mac e Linux.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')  # Pasta das imagens
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')  # Pasta dos sons
RECORDE_ARQ = path.join(path.dirname(__file__), 'recorde.txt')  # Arquivo onde o recorde fica salvo

# ===== Resolução =====
# O jogo foi pensado numa tela de 800x400. ESCALA = 2.4 deixa a tela com 1920x960,
# a largura inteira de uma tela Full HD. As imagens da pasta assets já foram feitas
# nesse tamanho.
ESCALA = 2.4


def px(valor):
    """Converte uma medida pensada para a tela de 800x400 em pixels da tela de verdade."""
    return int(valor * ESCALA)  # int(): pixel é sempre um número inteiro


# ===== Tela =====
WIDTH = px(800)  # Largura da tela (1920)
HEIGHT = px(400)  # Altura da tela (960)
FPS = 60  # Frames (quadros) por segundo
CHAO = px(340)  # Altura (y) do chão: é onde ficam os pés do astronauta
ASTRONAUTA_X = px(100)  # O astronauta fica sempre neste x; quem anda é o cenário

# ===== Física do pulo =====
VELOCIDADE_PULO = px(-13)  # Velocidade no começo do pulo (negativa = para cima)
QUEDA_RAPIDA = 4  # No ar, segurando a seta para baixo, a gravidade fica 4 vezes mais forte

# ===== Velocidade do cenário (pixels por frame) =====
VELOCIDADE_INICIAL = px(7)  # Velocidade no começo do jogo
VELOCIDADE_MAXIMA = px(14)  # A velocidade nunca passa disso
PONTOS_PARA_ACELERAR = 400  # A cada 400 pontos, a velocidade aumenta

# Tempo (em frames) que o jogador tem para reagir entre um obstáculo e outro.
# Quanto menor, mais difícil.
FOLGA = 12

# ===== Obstáculos =====
# Para cada tipo de obstáculo:
#   'imagem': chave da imagem no dicionário de assets
#   'base':   altura (y) da parte de baixo do obstáculo (o rect.bottom)
#             Mais que CHAO = enterrado no chão; menos que CHAO = voando.
#   'extra':  quanto ele anda a mais que o cenário (os que voam são mais rápidos)
#   'acao':   o que o jogador precisa fazer para passar: 'pular' ou 'abaixar'
OBSTACULOS = {
    # Ficam no chão
    'pedra': {'imagem': 'pedra', 'base': CHAO + px(6), 'extra': 0, 'acao': 'pular'},
    'pedras': {'imagem': 'pedras', 'base': CHAO + px(6), 'extra': 0, 'acao': 'pular'},
    'rocha_alta': {'imagem': 'rocha_alta', 'base': CHAO + px(4), 'extra': 0, 'acao': 'pular'},
    'cratera': {'imagem': 'cratera', 'base': CHAO + px(16), 'extra': 0, 'acao': 'pular'},  # Buraco: quase todo abaixo do chão
    'cratera_grande': {'imagem': 'cratera_grande', 'base': CHAO + px(19), 'extra': 0, 'acao': 'pular'},
    # Voam rasteiro, na altura dos pés
    'meteoro_baixo': {'imagem': 'meteoro', 'base': CHAO - px(4), 'extra': px(2), 'acao': 'pular'},
    'passaro_baixo': {'imagem': 'passaro', 'base': CHAO - px(6), 'extra': px(1), 'acao': 'pular'},
    # Voam na altura da cabeça
    'meteoro': {'imagem': 'meteoro', 'base': CHAO - px(44), 'extra': px(2), 'acao': 'abaixar'},
    'passaro': {'imagem': 'passaro', 'base': CHAO - px(44), 'extra': px(1), 'acao': 'abaixar'},
}

# ===== Planetas =====
# Cada planeta tem a sua gravidade e os seus obstáculos.
# Gravidade menor = pulo mais alto e mais demorado.
# Um tipo que aparece duas vezes na lista é sorteado com mais frequência.
PLANETAS = [
    {
        'nome': 'Terra',
        'gravidade': 0.8 * ESCALA,
        'obstaculos': ['pedra', 'pedra', 'pedras', 'cratera', 'passaro', 'passaro', 'passaro_baixo'],
        'mensagem': 'Terra: cuidado com os pássaros!',
        'ceu': 'ceu_terra.png',
        'chao': 'chao_terra.png',
    },
    {
        'nome': 'Lua',
        'gravidade': 0.55 * ESCALA,
        'obstaculos': ['pedra', 'pedras', 'cratera', 'cratera_grande', 'meteoro', 'meteoro', 'meteoro_baixo'],
        'mensagem': 'Lua: chuva de meteoros!',
        'ceu': 'ceu_lua.png',
        'chao': 'chao_lua.png',
    },
    {
        'nome': 'Marte',
        'gravidade': 0.6 * ESCALA,
        'obstaculos': ['pedras', 'rocha_alta', 'rocha_alta', 'cratera_grande', 'meteoro', 'meteoro', 'meteoro_baixo'],
        'mensagem': 'Marte: falta pouco!',
        'ceu': 'ceu_marte.png',
        'chao': 'chao_marte.png',
    },
]
DISTANCIA_PLANETA = px(15000)  # Quantos pixels o astronauta corre em cada planeta

# ===== Cores (vermelho, verde, azul) =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 40)

# ===== Estados da aplicação (qual tela está aberta) =====
INIT = 0  # Tela inicial
GAME = 1  # Partida
QUIT = 2  # Fechar o jogo
