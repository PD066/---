import pygame

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
]#создание_анимации_бега_врагов
attack_right = [
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)л/Attack_3.4.png').convert_alpha()
]#создание_анимации_атаки_влево
attack_left = [
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.1.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.2.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.3.png').convert_alpha(),
    pygame.image.load('ритм игра/images/анимация/атака(1)п/Attack_3.4.png').convert_alpha(),
]#создание_анимации_атаки_вправо
idle = [
pygame.image.load('ритм игра/images/анимация/афк/idle.1.png').convert_alpha(),
pygame.image.load('ритм игра/images/анимация/афк/idle.2.png').convert_alpha(),
pygame.image.load('ритм игра/images/анимация/афк/idle.3.png').convert_alpha(),
pygame.image.load('ритм игра/images/анимация/афк/idle.4.png').convert_alpha(),
pygame.image.load('ритм игра/images/анимация/афк/idle.5.png').convert_alpha(),
pygame.image.load('ритм игра/images/анимация/афк/idle.6.png').convert_alpha()
]#создание_анимации_афк
enemy_speed = 25#скорость_врагов
enemy_anim_count=0
enemy_list_in_game = []

player_anim_count = 0
player_anim_count2 = 0
player=pygame.Surface((128,128))

area=pygame.Surface((1500,50))
area.fill((73, 74, 73))

bg_sound = pygame.mixer.Sound('ритм игра\sounds\Yoshida Brothers - Rising.mp3')#вывод_звукового_сопровождения
bg_sound.play()
bg_sound.set_volume(0.1)

bg = pygame.image.load('ритм игра/images/фон.jpg').convert_alpha()#вывод_фона

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

running = True
while True:
    screen.blit(bg, (0, 0))
    screen.blit(area, (0, 750))

    player_rect = attack_left[0].get_rect(topleft=(686, 622))

    if enemy_list_in_game:
        for el in enemy_list_in_game:
            screen.blit(enemy_run[enemy_anim_count], el)
            el.x += 25

            if player_rect.colliderect(el):
                print('Ты проиграл')

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or  keys[pygame.K_a] :
        screen.blit(attack_left[player_anim_count], (686, 622))#привязка_клавиши

    elif keys[pygame.K_RIGHT] or  keys[pygame.K_d] :
        screen.blit(attack_right[player_anim_count], (686, 622))#привязка_клавиши
    else:
        screen.blit(idle[player_anim_count2], (686, 622))

    if player_anim_count2 == 5:
        player_anim_count2 = 0
    else:
        player_anim_count2 += 1

    if player_anim_count == 3:
        player_anim_count = 0
    else:
        player_anim_count += 1

    if  enemy_anim_count ==7 :
        enemy_anim_count = 0
    else:
        enemy_anim_count += 1

    pygame.display.update()
    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy_run[0].get_rect(topleft=(0,622)))


    clock.tick(10)
