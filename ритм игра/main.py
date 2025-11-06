import pygame

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('ритм игра')
icon = pygame.image.load('ритм игра/images/icon.png')
pygame.display.set_icon(icon)
player=pygame.Surface((128,128))
area=pygame.Surface((1500,135))
area.fill((73, 74, 73))
bg = pygame.image.load('ритм игра/images/фон.jpg')
running = True
while True:
    screen.blit(bg, (0,0))
    screen.blit(player, (750, 537))
    screen.blit(area, (0, 665))
    pygame.display.update()
    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


