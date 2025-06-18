import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# Load background
background = pygame.image.load("images/maps/MonkeyMeadow.png")

class RedBloon:
    def __init__(self, image_path, x, y, speed):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.speed = speed

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 1:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

bloon = RedBloon("images/bloons/redbloon.png", 100, 100, speed=5)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move the bloon toward the mouse
    bloon.move_toward(mouse_x, mouse_y)

    # Draw everything
    screen.blit(background, (0, 0))
    bloon.draw(screen)

    pygame.display.update()
    clock.tick(60)
