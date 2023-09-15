import pygame
import socket
import requests
import tkinter as tk
from tkinter import messagebox
import time
import random
import uuid

# Inicialização do pygame
pygame.init()

# Configurações da janela do jogo
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Coleta de informações da rede e localização
def get_network_info():
    host_name = socket.gethostname()
    local_ip = socket.gethostbyname(host_name)
    response = requests.get('https://ipinfo.io')
    location_info = response.json()
    machine_id = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return f"ID da Máquina: {machine_id}\nNome da Máquina: {host_name}\nIP Local: {local_ip}\nLocalização: {location_info['city']}, {location_info['region']}"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Raquetes
PLAYER_WIDTH, PLAYER_HEIGHT = 10, 100
player = pygame.Rect(50, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)

# Bola
BALL_WIDTH, BALL_HEIGHT = 15, 15
ball = pygame.Rect(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
ball_speed_x = 3
ball_speed_y = 3

# Fonte
font = pygame.font.Font(None, 36)

# Variáveis do jogo
player_score = 0
opponent_score = 0
game_duration = 30
start_time = time.time()
game_over = False

# Variável para controlar a rebatida da máquina
rebate_probability = 0.9  # Probabilidade de 90% de rebatida

# Velocidade de movimento do jogador
player_speed = 3

# Variável para controlar a mensagem de agradecimento
show_message = False

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtém a posição do cursor do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Define a posição do jogador com base na posição do cursor do mouse
    player.y = mouse_y

    # Lógica do jogo
    if not game_over:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Colisão com as bordas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # Colisão com as raquetes
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x = -ball_speed_x

        # Ponto da máquina
        if ball.left <= 0:
            opponent_score += 1
            ball = pygame.Rect(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
            ball_speed_x = 3  # Reiniciamos a velocidade da bola
            ball_speed_y = 3  # Reiniciamos a velocidade da bola

        # Ponto do jogador
        if ball.right >= WIDTH:
            player_score += 1
            ball = pygame.Rect(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
            ball_speed_x = 3  # Reiniciamos a velocidade da bola
            ball_speed_y = 3  # Reiniciamos a velocidade da bola

        # Rebate do jogador
        if ball.colliderect(player) and ball_speed_x < 0:
            ball_speed_x = -ball_speed_x

        # Rebate da máquina com 90% de probabilidade
        if random.random() <= rebate_probability:
            if opponent.centery < ball.centery:
                opponent.y += 3  # Movimento mais lento da raquete da máquina
            else:
                opponent.y -= 3  # Movimento mais lento da raquete da máquina

        # Encerra o jogo após 30 segundos
        if time.time() - start_time >= game_duration:
            game_over = True
            show_message = True  # Ativar a mensagem de agradecimento

    # Desenhar
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, player)
    pygame.draw.rect(window, WHITE, opponent)
    pygame.draw.ellipse(window, WHITE, ball)
    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    if game_over:
        game_over_text = font.render(f"Game Over. Pontuação: {player_score}", True, WHITE)
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()

    # Exibir a mensagem de agradecimento após 30 segundos
    if show_message:
        show_message = False  # Impedir a repetição da mensagem
        # Salvar dados em um arquivo txt
        data_to_save = get_network_info()
        with open("dados.txt", "w") as file:
            file.write(data_to_save)
        
        # Mostrar pop-up com mensagem de agradecimento
        root = tk.Tk()
        root.withdraw()
        message_text = "Obrigado pelos seus dados!! \n, ass:\n Budah"
        message_box = tk.messagebox.showinfo("Agradecimento", message_text)
        if message_box == 'ok':
            running = False  # Encerrar o jogo

# Encerre o jogo
pygame.quit()
