import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уклоняйся от препятствий")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Настройки игрока
player_size = 50


# Функция для сохранения результата в файл
def save_score(score):
    if not os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'w') as f:
            f.write("Leaderboard\n")

    with open('leaderboard.txt', 'a') as f:
        f.write(f'{score}\n')


# Функция для игры
def game_loop():
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    enemy_pos = [random.randint(0, WIDTH - player_size), 0]
    enemy_speed = 10
    clock = pygame.time.Clock()
    score = 0

    # Воспроизведение первой музыкальной дорожки
    pygame.mixer.music.load('music1.mp3')
    pygame.mixer.music.play(-1)  # зацикливаем музыку

    while True:
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Движение игрока
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 10
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
                player_pos[0] += 10

            # Обновление позиции препятствий
            enemy_pos[1] += enemy_speed
            if enemy_pos[1] >= HEIGHT:
                enemy_pos[1] = 0
                enemy_pos[0] = random.randint(0, WIDTH - player_size)
                score += 1  # Увеличиваем счет, когда препятствие проходит

            # Проверка на Collision
            if (player_pos[0] < enemy_pos[0] < player_pos[0] + player_size or
                player_pos[0] < enemy_pos[0] + player_size < player_pos[0] + player_size) and \
                    (player_pos[1] < enemy_pos[1] < player_pos[1] + player_size or
                     player_pos[1] < enemy_pos[1] + player_size < player_pos[1] + player_size):
                pygame.mixer.music.stop()  # Останавливаем первую музыку
                pygame.mixer.Sound('sound2.mp3').play()  # Проигрываем звук 2
                save_score(score)  # Сохраняем счет в таблицу лидеров
                game_over = True

            # Отрисовка объектов
            screen.fill(WHITE)
            pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))
            pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], player_size, player_size))

            # Отображение счета
            font = pygame.font.SysFont("monospace", 35)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # Обновление экрана
            pygame.display.update()
            clock.tick(30)

        # После окончания игры, отображаем сообщение и таблицу лидеров
        display_game_over(score)


# Функция для отображения таблицы лидеров
def display_leaderboard():
    screen.fill(WHITE)
    font = pygame.font.SysFont("monospace", 35)

    # Заголовок таблицы лидеров
    leaderboard_text = font.render("Leaderboard", True, BLACK)
    screen.blit(leaderboard_text, (WIDTH // 2 - 100, 50))

    # Чтение файла лидеров
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as f:
            lines = f.readlines()[1:]  # Пропускаем заголовок
        for index, line in enumerate(lines[-5:], start=0):  # Показываем последние 5 результатов
                score_text = font.render(line.strip(), True, BLACK)
                screen.blit(score_text, (WIDTH // 2 - 70, 100 + index * 30))

    pygame.display.update()
    pygame.time.delay(2000)


# Функция отображения экрана окончания игры
def display_game_over(score):
    while True:
        screen.fill(WHITE)
        font = pygame.font.SysFont("monospace", 50)
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        # Кнопка "Show Leaderboard"
        leaderboard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
        pygame.draw.rect(screen, GREEN, leaderboard_button)
        leaderboard_text = font.render("Show Leaderboard", True, BLACK)
        screen.blit(leaderboard_text, (WIDTH // 2 - 90, HEIGHT // 2 + 20))

        # Кнопка "Restart"
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(screen, GREEN, restart_button)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - 70, HEIGHT // 2 + 80))

        # Кнопка "Exit"
        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 50)
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (WIDTH // 2 - 40, HEIGHT // 2 + 140))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if leaderboard_button.collidepoint(event.pos):
                    display_leaderboard()  # Показываем таблицу лидеров
                if restart_button.collidepoint(event.pos):
                    game_loop()  # Перезапускаем игру
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()


# Запускаем игру
game_loop()
