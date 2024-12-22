import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уклоняйся от препятствий")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_size = 50


def save_score(player_name, score):
    if not os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'w') as f:
            f.write("Leaderboard\n")
    with open('leaderboard.txt', 'a') as f:
        f.write(f'{player_name}: {score}\n')


def draw_text(text, font, surface, x, y):
    textobj = font.render(text, True, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def game_loop(player_name):
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    enemy_pos = [random.randint(0, WIDTH - player_size), 0]
    enemy_speed = 10
    clock = pygame.time.Clock()
    score = 0

    while True:
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 10
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
                player_pos[0] += 10

            enemy_pos[1] += enemy_speed
            if enemy_pos[1] >= HEIGHT:
                enemy_pos[1] = 0
                enemy_pos[0] = random.randint(0, WIDTH - player_size)
                score += 1

            if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_size or
                player_pos[0] < enemy_pos[0] + player_size < player_pos[0] + player_size) and \
                    (player_pos[1] < enemy_pos[1] < player_pos[1] + player_size or
                     player_pos[1] < enemy_pos[1] + player_size < player_pos[1] + player_size):
                save_score(player_name, score)  # Сохраняем счет и имя игрока в таблицу лидеров
                game_over = True

            screen.fill(WHITE)
            pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))
            pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], player_size, player_size))

            font = pygame.font.SysFont("monospace", 35)
            draw_text(f"Score: {score}", font, screen, 10, 10)

            pygame.display.update()
            clock.tick(30)

    display_game_over(player_name, score)


def display_leaderboard():
    screen.fill(WHITE)
    font = pygame.font.SysFont("monospace", 35)
    draw_text("Leaderboard", font, screen, WIDTH // 2 - 100, 50)

    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as f:
            lines = f.readlines()[1:]  # Пропускаем заголовок
        for index, line in enumerate(lines[-5:], start=0):  # Показываем последние 5 результатов
            draw_text(line.strip(), font, screen, WIDTH // 2 - 100, 100 + index * 30)
