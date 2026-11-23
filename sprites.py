"""Classes do jogo: o astronauta, os obstáculos e a poeira da batida."""
import pygame
from config import WIDTH, CHAO, ASTRONAUTA_X, VELOCIDADE_PULO, QUEDA_RAPIDA, OBSTACULOS


class Astronauta(pygame.sprite.Sprite):
    """Jogador. Fica sempre no mesmo x e só se move para cima e para baixo."""

    def __init__(self, assets, gravidade):
        # Construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.assets = assets  # Guarda os assets para trocar de imagem e tocar o som do pulo
        self.gravidade = gravidade  # Muda quando o astronauta troca de planeta
        # O rect só guarda números inteiros, então a altura dos pés fica em self.y
        # (que aceita casas decimais) e depois é copiada para o rect.
        self.y = CHAO  # Começa com os pés no chão
        self.speedy = 0  # Velocidade vertical (negativa = subindo)
        self.abaixado = False  # True enquanto a seta para baixo está apertada
        self.escolhe_imagem()  # Define self.image, self.mask e self.rect

    def no_chao(self):
        """Devolve True se o astronauta está pisando no chão."""
        return self.y >= CHAO

    def pular(self):
        """Começa um pulo, mas só se o astronauta estiver no chão e em pé."""
        if self.no_chao() and not self.abaixado:
            self.speedy = VELOCIDADE_PULO  # Ganha velocidade para cima
            self.assets['pulo'].play()  # Toca o som do pulo

    def update(self):
        """Aplica a gravidade e escolhe a imagem certa. É chamado uma vez por frame."""
        # A gravidade aumenta a velocidade para baixo um pouco a cada frame
        self.speedy += self.gravidade
        # Segurando a seta para baixo no ar, cai mais rápido (igual ao dinossauro do Google):
        # soma a gravidade mais (QUEDA_RAPIDA - 1) vezes, então no total é QUEDA_RAPIDA vezes
        if self.abaixado and not self.no_chao():
            self.speedy += self.gravidade * (QUEDA_RAPIDA - 1)
        # A velocidade muda a posição
        self.y += self.speedy
        # Se chegou no chão, para de cair
        if self.no_chao():
            self.y = CHAO
            self.speedy = 0
        self.escolhe_imagem()

    def escolhe_imagem(self):
        """Escolhe a imagem (no ar, abaixado ou correndo) e posiciona o rect."""
        # Animação de corrida: a imagem muda a cada 90 milissegundos.
        # get_ticks() // 90 conta quantas vezes já se passaram 90 ms desde que o jogo abriu;
        # % 4 (resto da divisão por 4) faz a conta ir 0, 1, 2, 3, 0, 1, 2, 3...
        frame = pygame.time.get_ticks() // 90 % 4
        if not self.no_chao():
            self.image = self.assets['pulando']
        elif self.abaixado:
            self.image = self.assets['abaixado'][frame % 2]  # Só tem 2 imagens: 0, 1, 0, 1...
        else:
            self.image = self.assets['astronauta'][frame]

        # A imagem abaixada é menor, então a máscara (para a colisão) e o rect são refeitos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (ASTRONAUTA_X, int(self.y))  # Canto de baixo à esquerda: os pés


class Obstaculo(pygame.sprite.Sprite):
    """Obstáculo que nasce na direita da tela e anda para a esquerda."""

    def __init__(self, assets, tipo, velocidade):
        # Construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)

        dados = OBSTACULOS[tipo]  # Dicionário com a imagem, a base e a velocidade extra (config.py)
        self.imagens = assets[dados['imagem']]  # Lista de imagens (só o pássaro tem mais de uma)
        self.extra = dados['extra']  # Quanto anda a mais que o cenário
        self.acao = dados['acao']  # 'pular' ou 'abaixar'
        self.speedx = -(velocidade + self.extra)  # Negativa = anda para a esquerda

        self.image = self.imagens[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # Começa logo depois da borda direita da tela, com a base na altura do tipo
        self.rect.bottomleft = (WIDTH, dados['base'])

    def update(self):
        """Move o obstáculo, anima o pássaro e apaga o obstáculo quando sai da tela."""
        self.rect.x += self.speedx
        # Troca de imagem a cada 140 ms (mesma conta da corrida do astronauta).
        # Com uma imagem só, o resto da divisão por 1 é sempre 0: a imagem não muda.
        self.image = self.imagens[pygame.time.get_ticks() // 140 % len(self.imagens)]
        self.mask = pygame.mask.from_surface(self.image)
        # Se passou do lado esquerdo da tela, morre (sai de todos os grupos)
        if self.rect.right < 0:
            self.kill()


class Explosao(pygame.sprite.Sprite):
    """Nuvem de poeira da batida (mesma ideia da classe Explosion do handout)."""

    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.imagens = assets['poeira']  # Lista com as 6 imagens da poeira
        self.inicio = pygame.time.get_ticks()  # Momento em que a poeira apareceu
        self.image = self.imagens[0]
        self.rect = self.image.get_rect()
        self.rect.center = center  # A poeira aparece onde estava o astronauta

    def update(self):
        """Mostra a imagem certa da animação e some quando ela acaba."""
        # Cada imagem fica 70 ms na tela: depois de 70 ms vai para a imagem 1, depois de 140 ms para a 2...
        frame = (pygame.time.get_ticks() - self.inicio) // 70
        if frame < len(self.imagens):
            self.image = self.imagens[frame]
        else:
            self.kill()  # Acabou a animação: tchau poeira!
