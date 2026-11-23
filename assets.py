"""Carrega as imagens, os sons e as fontes do jogo num dicionário (os assets)."""
import pygame
from os import path
from config import px, IMG_DIR, SND_DIR, PLANETAS


def carrega_imagem(arquivo):
    """Carrega uma imagem da pasta img, com transparência."""
    # convert_alpha() prepara a imagem para ser desenhada rápido e mantém o fundo transparente
    return pygame.image.load(path.join(IMG_DIR, arquivo)).convert_alpha()


def carrega_animacao(nome, quantidade):
    """Carrega as imagens de uma animação (nome0.png, nome1.png, ...) numa lista."""
    imagens = []
    for i in range(quantidade):
        imagens.append(carrega_imagem('{}{}.png'.format(nome, i)))  # Ex.: 'passaro0.png', 'passaro1.png'
    return imagens


def load_assets():
    """Carrega todos os assets e devolve um dicionário com eles."""
    assets = {}

    # ----- Fundos: o céu (tela inteira) e o chão (faixa de baixo) de cada planeta
    # Ficam em listas na mesma ordem dos PLANETAS: assets['ceus'][0] é o céu da Terra.
    # convert() (sem alpha): o fundo não tem partes transparentes, assim desenha mais rápido.
    assets['ceus'] = []
    assets['chaos'] = []
    for planeta in PLANETAS:
        assets['ceus'].append(pygame.image.load(path.join(IMG_DIR, planeta['ceu'])).convert())
        assets['chaos'].append(pygame.image.load(path.join(IMG_DIR, planeta['chao'])).convert())

    # ----- Animações (listas de imagens que vão se alternando)
    assets['astronauta'] = carrega_animacao('astronauta', 4)  # Correndo
    assets['abaixado'] = carrega_animacao('abaixado', 2)  # Correndo abaixado
    assets['passaro'] = carrega_animacao('passaro', 2)  # Batendo as asas
    assets['poeira'] = carrega_animacao('poeira', 6)  # Poeira da batida

    # ----- Imagens sozinhas
    assets['pulando'] = carrega_imagem('astronauta_pulando.png')  # Astronauta no ar
    assets['bandeira'] = carrega_imagem('bandeira.png')  # Bandeira da tela de vitória

    # ----- Obstáculos que não se mexem
    # Ficam numa lista com uma imagem só. Assim a classe Obstaculo trata todos do
    # mesmo jeito (como animação), tanto o pássaro quanto a pedra.
    for nome in ['pedra', 'pedras', 'rocha_alta', 'cratera', 'meteoro']:
        assets[nome] = [carrega_imagem(nome + '.png')]
    # A cratera grande é a imagem da cratera esticada para um tamanho maior
    assets['cratera_grande'] = [pygame.transform.scale(assets['cratera'][0], (px(118), px(24)))]

    # ----- Fontes (None = fonte padrão do pygame; o número é o tamanho)
    assets['fonte_pequena'] = pygame.font.SysFont(None, px(32))
    assets['fonte_grande'] = pygame.font.SysFont(None, px(56))
    assets['fonte_titulo'] = pygame.font.SysFont(None, px(96))

    # ----- Sons
    pygame.mixer.music.load(path.join(SND_DIR, 'musica.ogg'))  # Música de fundo da partida
    pygame.mixer.music.set_volume(0.4)  # Volume da música (de 0 a 1)
    # Efeitos sonoros: assets['pulo'], assets['batida'], assets['fase'] e assets['vitoria']
    for nome in ['pulo', 'batida', 'fase', 'vitoria']:
        assets[nome] = pygame.mixer.Sound(path.join(SND_DIR, nome + '.wav'))

    return assets
