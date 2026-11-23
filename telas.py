"""Tela inicial, tela final e as funções que desenham textos e o cenário."""
import pygame
from config import px, FPS, WIDTH, CHAO, ASTRONAUTA_X, PLANETAS, RECORDE_ARQ
from config import WHITE, BLACK, YELLOW, ORANGE, GAME, QUIT


def desenha_texto(window, fonte, texto, cor, centro):
    """Desenha um texto com sombra preta, com o centro na posição indicada."""
    # Sombra: o mesmo texto em preto, um pouco para a direita e para baixo
    sombra = fonte.render(texto, True, BLACK)  # render cria uma imagem com o texto
    sombra_rect = sombra.get_rect()
    sombra_rect.center = (centro[0] + px(2), centro[1] + px(2))
    window.blit(sombra, sombra_rect)
    # Texto de verdade, por cima da sombra
    imagem = fonte.render(texto, True, cor)
    imagem_rect = imagem.get_rect()
    imagem_rect.center = centro
    window.blit(imagem, imagem_rect)


def desenha_cenario(window, assets, planeta, andou_ceu, andou_chao):
    """Desenha o céu e o chão do planeta, deslocados para a esquerda.

    andou_ceu e andou_chao: quantos pixels o céu e o chão já andaram.
    """
    # % WIDTH (resto da divisão pela largura da tela) faz a posição voltar para 0
    # toda vez que a imagem anda uma tela inteira. O sinal de menos joga para a esquerda.
    ceu_x = -(andou_ceu % WIDTH)
    chao_x = -(andou_chao % WIDTH)
    # Cada imagem é desenhada duas vezes, uma ao lado da outra. Assim, quando
    # o cenário anda para a esquerda, a tela continua toda preenchida.
    window.blit(assets['ceus'][planeta], (ceu_x, 0))
    window.blit(assets['ceus'][planeta], (ceu_x + WIDTH, 0))
    window.blit(assets['chaos'][planeta], (chao_x, CHAO))
    window.blit(assets['chaos'][planeta], (chao_x + WIDTH, CHAO))


def tela_parada(window, assets, planeta, textos, bandeira):
    """Mostra o cenário parado, o astronauta e os textos até apertar ESPAÇO ou fechar a janela.

    textos: lista de (chave da fonte, texto, cor, altura y do centro).
    bandeira: True para desenhar a bandeira ao lado do astronauta.
    Devolve o próximo estado: GAME (jogar) ou QUIT (fechar).
    """
    clock = pygame.time.Clock()  # Para controlar os frames por segundo
    # Só aceita o ESPAÇO depois de 1 segundo, para ninguém pular a tela sem querer
    inicio = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clicou no X da janela
                return QUIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() - inicio > 1000:
                    return GAME

        # ----- Gera saídas
        desenha_cenario(window, assets, planeta, 0, 0)  # 0, 0: cenário parado
        # Astronauta em pé no chão (primeira imagem da corrida)
        astronauta_rect = assets['astronauta'][0].get_rect()
        astronauta_rect.bottomleft = (ASTRONAUTA_X, CHAO)
        window.blit(assets['astronauta'][0], astronauta_rect)
        # Bandeira um pouco à direita do astronauta (só na vitória)
        if bandeira:
            bandeira_rect = assets['bandeira'].get_rect()
            bandeira_rect.bottomleft = (astronauta_rect.right + px(10), CHAO + px(4))
            window.blit(assets['bandeira'], bandeira_rect)
        # Textos centralizados na horizontal (x = metade da tela)
        for fonte, texto, cor, y in textos:
            desenha_texto(window, assets[fonte], texto, cor, (WIDTH / 2, y))

        pygame.display.update()  # Mostra o novo frame para o jogador


def init_screen(window, assets):
    """Tela inicial: nome do jogo e instruções no cenário da Terra."""
    textos = [
        ('fonte_titulo', 'ASTRONAUTA', YELLOW, px(80)),
        ('fonte_pequena', 'Atravesse a Terra, a Lua e Marte sem bater em nada!', WHITE, px(150)),
        ('fonte_pequena', 'ESPAÇO: pular        SETA PARA BAIXO: abaixar', WHITE, px(185)),
        ('fonte_pequena', 'No ar, SETA PARA BAIXO faz cair mais rápido', WHITE, px(215)),
        ('fonte_pequena', 'Aperte ESPAÇO para começar', YELLOW, px(270)),
    ]
    return tela_parada(window, assets, 0, textos, False)  # 0: cenário da Terra, sem bandeira


def end_screen(window, assets, score, venceu):
    """Tela final: resultado, pontos e recorde (salvo no arquivo recorde.txt)."""
    # ----- Lê o recorde do arquivo
    # Abrir com 'a' cria o arquivo se ele ainda não existir (e não apaga nada)
    with open(RECORDE_ARQ, 'a') as arquivo:
        arquivo.write('')
    with open(RECORDE_ARQ, 'r') as arquivo:
        conteudo = arquivo.read()
    recorde = 0  # Arquivo vazio: ainda não tem recorde
    if conteudo != '':
        recorde = int(conteudo)

    # ----- Se fez mais pontos que o recorde, salva o novo recorde ('w' apaga o anterior)
    if score > recorde:
        texto_recorde = ('fonte_pequena', 'NOVO RECORDE!', ORANGE, px(205))
        with open(RECORDE_ARQ, 'w') as arquivo:
            arquivo.write(str(score))
    else:
        texto_recorde = ('fonte_pequena', 'Recorde: {}'.format(recorde), WHITE, px(205))

    # ----- Título e fundo: Marte se venceu, Terra se perdeu
    if venceu:
        titulo = 'MISSÃO CUMPRIDA!'
        planeta = len(PLANETAS) - 1  # Último planeta (Marte)
    else:
        titulo = 'FIM DE JOGO'
        planeta = 0  # Primeiro planeta (Terra)

    textos = [
        ('fonte_titulo', titulo, YELLOW, px(80)),
        ('fonte_grande', 'Pontos: {}'.format(score), WHITE, px(160)),
        texto_recorde,
        ('fonte_pequena', 'Aperte ESPAÇO para jogar de novo', YELLOW, px(265)),
    ]
    return tela_parada(window, assets, planeta, textos, venceu)  # Bandeira só se venceu
