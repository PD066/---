import pygame
import random

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('ритм игра')
icon = pygame.image.load('ритм игра/images/icon.png').convert_alpha()
pygame.display.set_icon(icon)
enemy_run = [
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.4.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.5.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.6.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.7.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/бег_врагов/Run.8.png').convert_alpha()
]  # создание_анимации_бега_врагов
attack_right = [
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.4.png').convert_alpha()
]  # создание_анимации_атаки_влево
attack_left = [
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.4.png').convert_alpha(),
]  # создание_анимации_атаки_вправо
idle = [
    pygame.image.load('ритм игра/images/анимация/афк/idle.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.4.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.5.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/афк/idle.6.png').convert_alpha()
]  # создание_анимации_афк
enemy_speed = 25  # скорость_врагов
enemy_anim_count = 0

enemy_list_in_game = []

player_anim_count = 0
player_anim_count2 = 0
dead_anim_count = 0
player = pygame.Surface((128, 128))
score = 0

area = pygame.Surface((1500, 50))
area.fill((73, 74, 73))

bg_sound = pygame.mixer.Sound('ритм игра/sounds/Yoshida Brothers - Rising.mp3')  # вывод_звукового_сопровождения
bg_sound.play()
bg_sound.set_volume(0.1)

bg = pygame.image.load('ритм игра/images/фон.jpg').convert_alpha()  # вывод_фона

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)
dead_timer = pygame.USEREVENT +1
pygame.time.set_timer(dead_timer, 1000)

label = pygame.font.Font('ритм игра/fonts/ofont.ru_Celtes SP.ttf',40)
lose_label = label.render('Вы проиграли!', False,(107, 20, 6))
Restart_label = label.render('Играть занаво', False,(107, 20, 6))
Restart_label_rect = Restart_label.get_rect(topleft=(560, 450))

gameplay = True

running = True
while running:
    screen.blit(bg, (0, 0))
    screen.blit(area, (0, 750))

    if gameplay:

        player_rect = attack_left[0].get_rect(topleft=(686, 622))
        keys = pygame.key.get_pressed()

        if enemy_list_in_game:
            for enemy in enemy_list_in_game[:]:
                #Отрисовка_врага
                screen.blit(enemy_run[enemy_anim_count], enemy['rect'])

                if enemy['direction'] == 1:
                    enemy['rect'].x += enemy_speed  #Движение_вправо
                else:
                    enemy['rect'].x -= enemy_speed  #Движение_влево

                #Проверка_cтолкновения_c_игроком
                if player_rect.colliderect(enemy['rect']):
                    gameplay = False

                if enemy['direction'] == 1 and enemy['rect'].x > 686 and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                    score += 50
                    enemy_list_in_game.remove(enemy)
                elif enemy['direction'] == 0 and enemy['rect'].x < 814 and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                    score += 50
                    enemy_list_in_game.remove(enemy)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            screen.blit(attack_left[player_anim_count], (686, 622))  # привязка_клавиши

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            screen.blit(attack_right[player_anim_count], (686, 622))  # привязка_клавиши
        else:
            screen.blit(idle[player_anim_count2], (686, 622))

        if dead_anim_count == 5:
            dead_anim_count = 0
        else:
            dead_anim_count += 1

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
    else:
        screen.fill((105, 104, 104))
        screen.blit(lose_label, (560,330))
        screen.blit(Restart_label,Restart_label_rect)



        mouse = pygame.mouse.get_pos()
        if Restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            enemy_list_in_game.clear()

    pygame.display.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == enemy_timer:
            spawn = random.randint(0, 1)
            if spawn == 1:

                enemy_list_in_game.append({
                    'rect': enemy_run[0].get_rect(topleft=(0, 622)),
                    'direction': 1
                })
            else:

                enemy_list_in_game.append({
                    'rect': enemy_run[0].get_rect(topleft=(1500, 622)),
                    'direction': 0
                })

    clock.tick(10)

pygame.quit()
