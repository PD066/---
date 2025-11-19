import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('ритм игра')
icon = pygame.image.load('ритм игра/images/icon.png')
pygame.display.set_icon(icon)
attack_right = [
    pygame.image.load('ритм игра\images\анимация\атака(1)л\Attack_3.1.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)л\Attack_3.2.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)л\Attack_3.3.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)л\Attack_3.4.png')
]
attack_left = [
    pygame.image.load('ритм игра\images\анимация\атака(1)п\Attack_3.1.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)п\Attack_3.2.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)п\Attack_3.3.png'),
    pygame.image.load('ритм игра\images\анимация\атака(1)п\Attack_3.4.png'),
]
idle = [
pygame.image.load('ритм игра\images\анимация\афк\idle.1.png'),
pygame.image.load('ритм игра\images\анимация\афк\idle.2.png'),
pygame.image.load('ритм игра\images\анимация\афк\idle.3.png'),
pygame.image.load('ритм игра\images\анимация\афк\idle.4.png'),
pygame.image.load('ритм игра\images\анимация\афк\idle.5.png'),
pygame.image.load('ритм игра\images\анимация\афк\idle.6.png')
]
enemy_speed = 5
enemy_right_x = 0
player_anim_count = 0
player_anim_count2 = 0
player=pygame.Surface((128,128))
area=pygame.Surface((1500,50))
area.fill((73, 74, 73))
bg_sound = pygame.mixer.Sound('ритм игра\sounds\Yoshida Brothers - Rising.mp3')
bg_sound.play()
bg_sound.set_volume(0.3)
bg = pygame.image.load('ритм игра/images/фон.jpg')
running = True
while True:
    screen.blit(bg, (0, 0))
    screen.blit(area, (0, 750))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] :
        screen.blit(attack_left[player_anim_count], (686, 622))

    elif keys[pygame.K_RIGHT]:
        screen.blit(attack_right[player_anim_count], (686, 622))
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


    pygame.display.update()
    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    clock.tick(10)


