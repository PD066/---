import pygame
import random

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('Bushido Blade')
icon = pygame.image.load('ритм игра/images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

# Загрузка анимаций
enemy_run_right = [
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.4.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.5.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.6.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.7.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.8.png').convert_alpha()
]

# Создаем зеркальные спрайты для движения влево
enemy_run_left = [pygame.transform.flip(img, True, False) for img in enemy_run_right]

attack_right = [
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.4.png').convert_alpha()
]

attack_left = [
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.4.png').convert_alpha(),
]

idle = [
    pygame.image.load('ритм игра/images/анимация/афк/idle.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.4.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.5.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.6.png').convert_alpha()
]

# Инициализация переменных
enemy_speed = 25
enemy_anim_count = 0
enemy_list_in_game = []
player_anim_count = 0
player_anim_count2 = 0
score = 0
final_score = 0

# Параметры атаки
attack_range = 120
attack_cooldown = 0
attack_cooldown_max = 5
is_attacking = False
last_attack_direction = 0

# Хитбоксы
player_hitbox_width = 80
player_hitbox_height = 80
player_hitbox_offset_x = 24
player_hitbox_offset_y = 24

enemy_hitbox_width = 80
enemy_hitbox_height = 80
enemy_hitbox_offset_x = 24
enemy_hitbox_offset_y = 24

area = pygame.Surface((1500, 50))
area.fill((73, 74, 73))

# Загрузка музыки
bg_sound = pygame.mixer.Sound('ритм игра/sounds/Yoshida Brothers - Rising.mp3')
bg_sound.set_volume(0.1)
music_playing = False

bg = pygame.image.load('ритм игра/images/фон.jpg').convert_alpha()

enemy_timer = pygame.USEREVENT + 1

# Шрифты для текста
label = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf', 40)
score_font = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf', 36)
final_score_font = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf', 48)
menu_font = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf', 60)
title_font = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf', 80)

# Состояния игры
MAIN_MENU = 0
GAMEPLAY = 1
GAME_OVER = 2
game_state = MAIN_MENU

running = True


# Функция для управления музыкой
def manage_music(state):
    global music_playing
    if state and not music_playing:
        bg_sound.play(-1)
        music_playing = True
    elif not state and music_playing:
        bg_sound.stop()
        music_playing = False


# Функция для проверки атаки
def check_attack(player_center, enemy_center, direction):
    # Вычисляем расстояние между игроком и врагом
    distance = abs(player_center[0] - enemy_center[0])

    # Проверяем дистанцию атаки
    if distance <= attack_range:
        # Проверяем направление атаки
        if direction == 1:  # Атака влево
            # Враг должен быть слева от игрока
            if enemy_center[0] < player_center[0]:
                return True
        elif direction == 2:  # Атака вправо
            # Враг должен быть справа от игрока
            if enemy_center[0] > player_center[0]:
                return True
    return False


# Функция для получения центра хитбокса
def get_hitbox_center(rect, offset_x, offset_y, width, height):
    hitbox_x = rect.x + offset_x
    hitbox_y = rect.y + offset_y
    return (hitbox_x + width // 2, hitbox_y + height // 2)


# Функция для сброса игры
def reset_game():
    global enemy_list_in_game, score, final_score, attack_cooldown, enemy_anim_count
    global player_anim_count, player_anim_count2
    enemy_list_in_game.clear()
    score = 0
    final_score = 0
    attack_cooldown = 0
    enemy_anim_count = 0
    player_anim_count = 0
    player_anim_count2 = 0


# Функция для отрисовки главного меню
def draw_main_menu():
    # Темный фон
    screen.fill((20, 15, 10))

    # Добавляем градиентный фон
    for i in range(800):
        color_value = max(20, 50 - i // 20)
        pygame.draw.line(screen, (color_value, color_value - 10, color_value - 15), (0, i), (1500, i))

    # Заголовок игры
    title_text = title_font.render('BUSHIDO BLADE', True, (180, 30, 30))
    title_shadow = title_font.render('BUSHIDO BLADE', True, (80, 10, 10))
    title_rect = title_text.get_rect(center=(750, 200))

    # Рисуем тень
    shadow_rect = title_shadow.get_rect(center=(754, 204))
    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)

    # Подзаголовок
    subtitle = label.render('ПУТЬ ВОИНА', True, (200, 180, 100))
    subtitle_rect = subtitle.get_rect(center=(750, 280))
    screen.blit(subtitle, subtitle_rect)

    # Кнопка "Начать битву"
    start_text = menu_font.render('НАЧАТЬ БИТВУ', True, (220, 50, 50))
    start_rect = start_text.get_rect(center=(750, 400))
    screen.blit(start_text, start_rect)

    # Кнопка "Выход"
    exit_text = menu_font.render('ВЫХОД', True, (150, 150, 150))
    exit_rect = exit_text.get_rect(center=(750, 500))
    screen.blit(exit_text, exit_rect)

    # Подсказка управления
    controls_hint1 = label.render('УПРАВЛЕНИЕ:', True, (180, 160, 140))
    controls_hint2 = label.render('A - УДАР СЛЕВА', True, (180, 160, 140))
    controls_hint3 = label.render('D - УДАР СПРАВА', True, (180, 160, 140))

    controls_rect1 = controls_hint1.get_rect(center=(750, 620))
    controls_rect2 = controls_hint2.get_rect(center=(750, 670))
    controls_rect3 = controls_hint3.get_rect(center=(750, 720))

    screen.blit(controls_hint1, controls_rect1)
    screen.blit(controls_hint2, controls_rect2)
    screen.blit(controls_hint3, controls_rect3)

    return start_rect, exit_rect


# Функция для отрисовки экрана проигрыша
def draw_game_over():
    # Темный фон
    screen.fill((30, 20, 15))

    # Градиент
    for i in range(800):
        color_value = max(30, 60 - i // 15)
        pygame.draw.line(screen, (color_value + 10, color_value - 5, color_value - 10), (0, i), (1500, i))

    # Надпись "ПОРАЖЕНИЕ"
    lose_label = menu_font.render('ПОРАЖЕНИЕ', False, (180, 30, 30))
    lose_shadow = menu_font.render('ПОРАЖЕНИЕ', False, (80, 10, 10))
    lose_label_rect = lose_label.get_rect(center=(750, 200))

    # Тень
    lose_shadow_rect = lose_shadow.get_rect(center=(754, 204))
    screen.blit(lose_shadow, lose_shadow_rect)
    screen.blit(lose_label, lose_label_rect)

    # Финальный счет
    final_score_text = final_score_font.render(f'Ваш счет: {final_score}', True, (220, 180, 60))
    final_score_rect = final_score_text.get_rect(center=(750, 350))
    screen.blit(final_score_text, final_score_rect)

    # Кнопка "Играть заново"
    restart_text = menu_font.render('НОВАЯ БИТВА', True, (220, 50, 50))
    restart_rect = restart_text.get_rect(center=(750, 470))
    screen.blit(restart_text, restart_rect)

    # Кнопка "Главное меню"
    menu_text = menu_font.render('ГЛАВНОЕ МЕНЮ', True, (150, 150, 150))
    menu_rect = menu_text.get_rect(center=(750, 570))
    screen.blit(menu_text, menu_rect)

    return restart_rect, menu_rect


while running:
    screen.blit(bg, (0, 0))

    if game_state == MAIN_MENU:
        # Отрисовка главного меню
        start_button, exit_button = draw_main_menu()

        # Обработка кликов в меню
        mouse = pygame.mouse.get_pos()

        # Подсветка кнопок при наведении
        if start_button.collidepoint(mouse):
            pygame.draw.rect(screen, (220, 50, 50), start_button.inflate(30, 15), 3, border_radius=8)
        if exit_button.collidepoint(mouse):
            pygame.draw.rect(screen, (100, 100, 100), exit_button.inflate(30, 15), 3, border_radius=8)

        # Обработка кликов
        if pygame.mouse.get_pressed()[0]:
            if start_button.collidepoint(mouse):
                reset_game()
                game_state = GAMEPLAY
                pygame.time.set_timer(enemy_timer, 1000)
                manage_music(True)
            elif exit_button.collidepoint(mouse):
                running = False

    elif game_state == GAMEPLAY:
        screen.blit(area, (0, 750))

        # Создаем базовый rect для игрока
        player_base_rect = attack_left[0].get_rect(topleft=(686, 622))

        # Создаем хитбокс игрока
        player_hitbox = pygame.Rect(
            player_base_rect.x + player_hitbox_offset_x,
            player_base_rect.y + player_hitbox_offset_y,
            player_hitbox_width,
            player_hitbox_height
        )

        # Получаем центр хитбокса игрока
        player_center = get_hitbox_center(
            player_base_rect,
            player_hitbox_offset_x,
            player_hitbox_offset_y,
            player_hitbox_width,
            player_hitbox_height
        )

        keys = pygame.key.get_pressed()

        # Обработка атаки
        is_attacking = False
        current_attack_direction = 0

        if attack_cooldown > 0:
            attack_cooldown -= 1

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            screen.blit(attack_left[player_anim_count], (686, 622))
            is_attacking = True
            current_attack_direction = 1
            last_attack_direction = 1

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            screen.blit(attack_right[player_anim_count], (686, 622))
            is_attacking = True
            current_attack_direction = 2
            last_attack_direction = 2
        else:
            screen.blit(idle[player_anim_count2], (686, 622))

        # Обработка врагов
        if enemy_list_in_game:
            for enemy in enemy_list_in_game[:]:
                # Выбираем правильную анимацию в зависимости от направления
                if enemy['direction'] == 1:  # Движение вправо
                    enemy_sprite = enemy_run_right[enemy_anim_count]
                else:  # Движение влево
                    enemy_sprite = enemy_run_left[enemy_anim_count]

                # Отрисовка врага
                screen.blit(enemy_sprite, enemy['rect'])

                # Создаем хитбокс врага
                enemy_hitbox = pygame.Rect(
                    enemy['rect'].x + enemy_hitbox_offset_x,
                    enemy['rect'].y + enemy_hitbox_offset_y,
                    enemy_hitbox_width,
                    enemy_hitbox_height
                )

                # Получаем центр хитбокса врага
                enemy_center = get_hitbox_center(
                    enemy['rect'],
                    enemy_hitbox_offset_x,
                    enemy_hitbox_offset_y,
                    enemy_hitbox_width,
                    enemy_hitbox_height
                )

                # Движение врага
                if enemy['direction'] == 1:
                    enemy['rect'].x += enemy_speed  # Движение вправо
                else:
                    enemy['rect'].x -= enemy_speed  # Движение влево

                # Проверка столкновения с игроком
                if player_hitbox.colliderect(enemy_hitbox):
                    game_state = GAME_OVER
                    final_score = score
                    manage_music(False)
                    pygame.time.set_timer(enemy_timer, 0)

                # Проверка атаки
                if is_attacking and attack_cooldown == 0:
                    if check_attack(player_center, enemy_center, current_attack_direction):
                        score += 50
                        enemy_list_in_game.remove(enemy)
                        attack_cooldown = attack_cooldown_max

                # Авто-удаление врагов
                if enemy['rect'].x < -200 or enemy['rect'].x > 1700:
                    enemy_list_in_game.remove(enemy)

        # Анимации
        if player_anim_count2 == 5:
            player_anim_count2 = 0
        else:
            player_anim_count2 += 1

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if enemy_anim_count == 7:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        # Отображение счета во время игры
        score_text = score_font.render(f'Счёт: {score}', True, (220, 50, 50))
        screen.blit(score_text, (20, 20))

    elif game_state == GAME_OVER:
        # Отрисовка экрана проигрыша
        restart_button, menu_button = draw_game_over()

        # Обработка кликов на экране проигрыша
        mouse = pygame.mouse.get_pos()

        # Подсветка кнопок при наведении
        if restart_button.collidepoint(mouse):
            pygame.draw.rect(screen, (220, 50, 50), restart_button.inflate(30, 15), 3, border_radius=8)
        if menu_button.collidepoint(mouse):
            pygame.draw.rect(screen, (100, 100, 100), menu_button.inflate(30, 15), 3, border_radius=8)

        # Обработка кликов
        if pygame.mouse.get_pressed()[0]:
            if restart_button.collidepoint(mouse):
                reset_game()
                game_state = GAMEPLAY
                pygame.time.set_timer(enemy_timer, 1000)
                manage_music(True)
            elif menu_button.collidepoint(mouse):
                reset_game()
                game_state = MAIN_MENU
                manage_music(False)

    pygame.display.update()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            manage_music(False)

        # Спавн врагов только во время игры
        if event.type == enemy_timer and game_state == GAMEPLAY:
            spawn = random.randint(0, 1)
            if spawn == 1:
                # Враг появляется слева и бежит вправо
                enemy_list_in_game.append({
                    'rect': enemy_run_right[0].get_rect(topleft=(0, 622)),
                    'direction': 1  # Движение вправо
                })
            else:
                # Враг появляется справа и бежит влево
                enemy_list_in_game.append({
                    'rect': enemy_run_left[0].get_rect(topleft=(1500, 622)),
                    'direction': 0  # Движение влево
                })

    clock.tick(10)

pygame.quit()
