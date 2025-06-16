import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
image = pygame.image.load("btd6/images/maps/MonkeyMeadow.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #draw everything
    screen.blit(image, (0,0))

    #do everything
    
    pygame.display.update()
    clock.tick(60)