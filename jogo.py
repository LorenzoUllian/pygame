"""Astronauta: jogo de corrida infinita feito com pygame.

Arquivo principal: inicia o pygame, cria a janela e troca entre as telas.
Para jogar, rode: python jogo.py
"""
# ===== Inicialização =====
# ----- Importa e inicia pacotes
import os
# No Windows com zoom de tela (125%, 150%...), esta linha evita que o Windows
# estique a janela do jogo e deixe tudo borrado. Precisa vir antes do import do pygame.
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
import pygame
from config import WIDTH, HEIGHT, INIT, GAME, QUIT
from assets import load_assets
from telas import init_screen
from game_screen import game_screen

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
# pygame.SCALED ajusta o tamanho da imagem do jogo à tela do computador.
# pygame.RESIZABLE deixa maximizar a janela (o jogo aumenta junto).
# vsync=1 mostra cada frame só quando o monitor está pronto para desenhar a tela.
# Sem isso, o monitor às vezes mostra metade de um frame e metade do outro, e o que
# anda rápido aparece "rasgado" e tremido, difícil de acompanhar com os olhos.
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED + pygame.RESIZABLE, vsync=1)
pygame.display.set_caption('Astronauta')

# ----- Carrega imagens, sons e fontes uma vez só (todas as telas usam o mesmo dicionário)
assets = load_assets()

# ===== Loop das telas (máquina de estados) =====
# Cada tela roda até o jogador sair dela e devolve qual é a próxima tela.
state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window, assets)
    elif state == GAME:
        state = game_screen(window, assets)  # Partida + tela final

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
