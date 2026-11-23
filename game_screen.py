"""Tela do jogo: o loop principal da partida."""
import random
import pygame
from config import FPS, WIDTH, ESCALA, px, PLANETAS, OBSTACULOS, DISTANCIA_PLANETA, VELOCIDADE_PULO, FOLGA
from config import VELOCIDADE_INICIAL, VELOCIDADE_MAXIMA, PONTOS_PARA_ACELERAR, WHITE, YELLOW, QUIT
from sprites import Astronauta, Obstaculo, Explosao
from telas import desenha_cenario, desenha_texto, end_screen


def game_screen(window, assets):
    """Roda uma partida e depois a tela final. Devolve o próximo estado (GAME ou QUIT)."""
    clock = pygame.time.Clock()  # Para controlar os frames por segundo

    # Grupos de sprites: all_sprites para desenhar, all_obstacles para testar a colisão
    all_sprites = pygame.sprite.Group()
    all_obstacles = pygame.sprite.Group()

    # O jogo começa no primeiro planeta (Terra)
    planeta_atual = 0  # Índice do planeta na lista PLANETAS
    planeta = PLANETAS[planeta_atual]  # Dicionário com os dados do planeta

    # Cria o jogador com a gravidade da Terra
    player = Astronauta(assets, planeta['gravidade'])
    all_sprites.add(player)

    # Estados da partida
    DONE = 0  # Acabou (vai para a tela final)
    PLAYING = 1  # Jogando
    EXPLODING = 2  # Bateu: mostrando a poeira antes de acabar
    state = PLAYING

    score = 0  # Pontos: 1 por frame
    venceu = False  # Vira True quando chega no fim de Marte
    distancia = 0  # Quantos pixels o astronauta já correu no planeta atual
    proximo_obstaculo = px(400)  # Distância em que vai nascer o próximo obstáculo
    # O tipo do próximo obstáculo é sorteado antes, porque o espaço até ele depende do tipo
    proximo_tipo = random.choice(planeta['obstaculos'])
    mensagem_tick = pygame.time.get_ticks()  # Momento em que a mensagem do planeta apareceu

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)  # Toca a música sem parar (loops=-1: repete sempre)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clicou no X da janela
                return QUIT
            # Apertou uma tecla (só vale enquanto está jogando)
            if event.type == pygame.KEYDOWN and state == PLAYING:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.pular()
                if event.key == pygame.K_DOWN:
                    player.abaixado = True  # No chão ele abaixa; no ar ele cai mais rápido
            # Soltou a seta para baixo
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                player.abaixado = False

        # ----- Atualiza estado do jogo
        if state == PLAYING:
            # Velocidade: aumenta ESCALA (2.4) pixels a cada 400 pontos, até o máximo
            velocidade = VELOCIDADE_INICIAL + (score // PONTOS_PARA_ACELERAR) * ESCALA
            if velocidade > VELOCIDADE_MAXIMA:
                velocidade = VELOCIDADE_MAXIMA
            velocidade = int(velocidade)  # int(): a posição dos sprites é sempre um número inteiro
            # Todos os obstáculos andam com a nova velocidade (mais a velocidade extra de cada um)
            for obstaculo in all_obstacles:
                obstaculo.speedx = -(velocidade + obstaculo.extra)

            all_sprites.update()  # Chama o update() de cada sprite (gravidade, movimento, animação)
            distancia += velocidade  # O cenário andou
            score += 1

            # Cria um novo obstáculo quando chega a distância sorteada.
            # Perto do fim do planeta não cria mais, para a tela ficar livre na troca.
            if distancia >= proximo_obstaculo and distancia < DISTANCIA_PLANETA - WIDTH:
                obstaculo = Obstaculo(assets, proximo_tipo, velocidade)
                all_sprites.add(obstaculo)
                all_obstacles.add(obstaculo)
                proximo_tipo = random.choice(planeta['obstaculos'])  # Já sorteia o próximo

                # Espaço mínimo até o próximo: a largura deste obstáculo mais o caminho que
                # o cenário anda durante o tempo de reação do jogador (FOLGA, em frames).
                # Assim, sequências intercaladas (pular e abaixar) vêm logo em seguida:
                # quem passou abaixado já está no chão, e quem pulou e precisa abaixar
                # segura a seta para baixo no ar, cai rápido e já chega abaixado.
                espaco = obstaculo.rect.width + velocidade * FOLGA
                # Mas dois de pular seguidos precisam de mais espaço: o astronauta
                # precisa cair do primeiro pulo antes de chegar no próximo.
                if obstaculo.acao == 'pular' and OBSTACULOS[proximo_tipo]['acao'] == 'pular':
                    frames_no_ar = 2 * -VELOCIDADE_PULO / planeta['gravidade']  # Duração do pulo (em frames)
                    espaco += velocidade * frames_no_ar
                # Se o próximo for mais rápido que este, ele vai chegando perto pelo
                # caminho. Por isso precisa nascer um pouco mais longe.
                diferenca = OBSTACULOS[proximo_tipo]['extra'] - obstaculo.extra
                if diferenca > 0:
                    espaco += diferenca * WIDTH / velocidade
                espaco = int(espaco)  # randint só aceita números inteiros
                # Sorteia onde nasce o próximo: entre o espaço mínimo e 250 (vezes ESCALA) pixels a mais
                proximo_obstaculo = distancia + random.randint(espaco, espaco + px(250))

            # Terminou o planeta: vence o jogo (se era Marte) ou vai para o próximo
            if distancia >= DISTANCIA_PLANETA:
                if planeta_atual == len(PLANETAS) - 1:
                    venceu = True
                    assets['vitoria'].play()
                    state = DONE
                else:
                    planeta_atual += 1
                    planeta = PLANETAS[planeta_atual]
                    player.gravidade = planeta['gravidade']  # O pulo muda com a gravidade
                    distancia = 0  # Recomeça a contar a distância no planeta novo
                    proximo_obstaculo = px(400)
                    proximo_tipo = random.choice(planeta['obstaculos'])
                    mensagem_tick = pygame.time.get_ticks()  # Mostra a mensagem do planeta novo
                    assets['fase'].play()

            # Verifica se o astronauta bateu em algum obstáculo.
            # collide_mask compara os pixels de verdade (a máscara), não só os retângulos.
            hits = pygame.sprite.spritecollide(player, all_obstacles, False, pygame.sprite.collide_mask)
            if len(hits) > 0:
                assets['batida'].play()
                player.kill()  # Tira o astronauta da tela
                explosao = Explosao(player.rect.center, assets)  # Poeira no lugar dele
                all_sprites.add(explosao)
                explosion_tick = pygame.time.get_ticks()  # Momento da batida
                state = EXPLODING

        elif state == EXPLODING:
            # Depois da batida, só a poeira se mexe (o cenário e os obstáculos param)
            explosao.update()
            # Espera 1 segundo para dar tempo de ver a poeira
            if pygame.time.get_ticks() - explosion_tick > 1000:
                state = DONE

        # ----- Gera saídas
        # O céu anda 2 pixels (px(1)) por ponto, mais devagar que o chão: dá profundidade
        desenha_cenario(window, assets, planeta_atual, score * px(1), distancia)
        all_sprites.draw(window)  # Desenha o astronauta, os obstáculos e a poeira

        # Placar (com 5 dígitos: 00042) e nome do planeta
        desenha_texto(window, assets['fonte_pequena'], '{:05d}'.format(score), WHITE, (WIDTH - px(60), px(25)))
        desenha_texto(window, assets['fonte_pequena'], planeta['nome'], WHITE, (px(60), px(25)))

        # Barra de progresso até o fim do planeta: a parte amarela cresce com a distância
        largura_barra = px(200) * distancia // DISTANCIA_PLANETA
        pygame.draw.rect(window, YELLOW, (px(110), px(18), largura_barra, px(14)))
        pygame.draw.rect(window, WHITE, (px(110), px(18), px(200), px(14)), px(2))  # Contorno

        # Mensagem do planeta nos primeiros 2,5 segundos (2500 ms)
        if pygame.time.get_ticks() - mensagem_tick < 2500:
            desenha_texto(window, assets['fonte_grande'], planeta['mensagem'], YELLOW, (WIDTH / 2, px(120)))

        pygame.display.update()  # Mostra o novo frame para o jogador

    pygame.mixer.music.stop()  # A música é só durante a partida
    return end_screen(window, assets, score, venceu)
