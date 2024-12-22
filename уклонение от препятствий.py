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
def save_score(player_name, score):
    if not os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'w') as f:
            f.write("Leaderboard\n")

    with open('leaderboard.txt', 'a') as f:
        f.write(f'{player_name}: {score}\n')


# Функция для отрисовки текста
def draw_text(text, font, surface, x, y):
    textobj = font.render(text, True, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Функция для запуска основной игры
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
                save_score(player_name, score)  # Сохраняем счет и имя игрока в таблицу лидеров
                game_over = True

            # Отрисовка объектов
            screen.fill(WHITE)
            pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))
            pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], player_size, player_size))

            # Отображение счета
            font = pygame.font.SysFont("monospace", 35)
            draw_text(f"Score: {score}", font, screen, 10, 10)

            # Обновление экрана
            pygame.display.update()
            clock.tick(30)

        # После окончания игры, отображаем сообщение и таблицу лидеров
    display_game_over(player_name, score)


# Функция для отображения таблицы лидеров
def display_leaderboard():
    screen.fill(WHITE)
    font = pygame.font.SysFont("monospace", 35)

    # Заголовок таблицы лидеров
    draw_text("Leaderboard", font, screen, WIDTH // 2 - 100, 50)

    # Чтение файла лидеров
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as f:
            lines = f.readlines()[1:]  # Пропускаем заголовок

        for index, line in enumerate(lines[-5:], start=0):  # Показываем последние 5 результатов
            draw_text(line.strip(), font, screen, WIDTH // 2 - 100, 100 + index * 30)
    else:
        draw_text("Нет результатов", font, screen, WIDTH // 2 - 100, 100)

    pygame.display.update()
    pygame.time.delay(2000)

    # Функция отображения экрана окончания игры
    def display_game_over(player_name, score):
        while True:
            screen.fill(WHITE)
            font = pygame.font.SysFont("monospace", 50)
            draw_text("Game Over!", font, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)

            # Кнопка "Show Leaderboard"
            leaderboard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
            pygame.draw.rect(screen, GREEN, leaderboard_button)
            draw_text("Show Leaderboard", font, screen, WIDTH // 2 - 90, HEIGHT // 2 + 20)

            # Кнопка "Restart"
            restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
            pygame.draw.rect(screen, GREEN, restart_button)
            draw_text("Restart", font, screen, WIDTH // 2 - 70, HEIGHT // 2 + 80)

            # Кнопка "Exit"
            exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 50)
            pygame.draw.rect(screen, RED, exit_button)
            draw_text("Exit", font, screen, WIDTH // 2 - 40, HEIGHT // 2 + 140)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if leaderboard_button.collidepoint(event.pos):
                        display_leaderboard()  # Показываем таблицу лидеров
                    if restart_button.collidepoint(event.pos):
                        game_intro()  # Перезапускаем игру
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()

            pygame.display.update()

    # Функция для ввода имени игрока
    def game_intro():
        player_name = ""
        font = pygame.font.SysFont("monospace", 35)

        while True:
            screen.fill(WHITE)
            draw_text(f"Введите ваше имя: {player_name}", font, screen, WIDTH // 2 - 200, HEIGHT // 2 - 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name:  # Если нажата Enter
                        game_loop(player_name)  # Запустим игру с именем игрока
                    elif event.key == pygame.K_BACKSPACE:  # Удаление последнего символа
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode  # Добавление символа к имени

            pygame.display.update()

    def play_background_music():
        pygame.mixer.music.load("background_music.mp3")  # Замените на название вашего музыкального файла
        pygame.mixer.music.play(-1)  # -1 для бесконечного воспроизведения

    # Запускаем ввод имени игрока и воспроизведение музыки
    play_background_music()  # Запускаем фоновую музыку
    game_intro()