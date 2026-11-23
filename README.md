# Astronauta

Jogo de corrida infinita em 2D feito com pygame para o Projeto Final de Design de Software (Insper).

O astronauta corre sozinho pela Terra, pela Lua e por Marte. O jogador precisa pular pedras e crateras e se abaixar para desviar de meteoros. Cada planeta tem uma gravidade diferente, então o pulo muda de altura. Chegando ao fim de Marte, a missão está cumprida.

## Integrantes

Lorenzo Calio Ullian
Caio takeda Marquesine
BERNARDO NIEDERAUER PRATES

## Como rodar

1. Instale o pygame-ce (a versão do pygame que funciona no Python 3.14 e 3.15): `python -m pip install pygame-ce`
2. Na pasta do projeto, rode: `python jogo.py`

## Controles

| Tecla | Ação |
| --- | --- |
| ESPAÇO ou seta para cima | Pular |
| Seta para baixo (segurar) | Abaixar (no ar: cair mais rápido) |
## Vídeo

LINK DO VÍDEO

## Organização do código

| Arquivo | O que faz |
| --- | --- |
| `jogo.py` | Arquivo principal: inicia o pygame, carrega os assets e troca entre as telas (máquina de estados) |
| `config.py` | Constantes: tamanhos, cores, física do pulo, tabela de obstáculos e dados de cada planeta |
| `assets.py` | Carrega imagens, sons e fontes num dicionário |
| `sprites.py` | Classes `Astronauta`, `Obstaculo` e `Explosao` |
| `game_screen.py` | Loop principal da partida |
| `telas.py` | Tela inicial, tela final (com o recorde salvo em `recorde.txt`) e as funções que desenham textos e o cenário |

A estrutura segue o handout de pygame da disciplina. As partes novas são:

- Pulo com gravidade: a cada frame, a gravidade do planeta é somada à velocidade vertical do astronauta.
- Queda rápida: segurando a seta para baixo no ar, a gravidade fica mais forte.
- Velocidade que aumenta com os pontos, como no jogo do dinossauro do Google.
- Sequências intercaladas: quando um obstáculo de pular e um de abaixar vêm seguidos (ou dois de abaixar), o segundo vem logo em seguida. Para pular e logo depois abaixar, é preciso usar a queda rápida.
