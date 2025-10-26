import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption('ритм игра')
icon = pygame.image.load('ритм игра/images/icon.png')
pygame.display.set_icon(icon)

running = True
while True:
    screen.fill((87, 8, 18))
    pygame.display.update()
    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

