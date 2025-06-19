import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Bloons TD 6')
clock = pygame.time.Clock()


# Colors
brown = (193,152,95)
darkbrown = (122,92,59)

# Load background
map = pygame.image.load("images/maps/MonkeyMeadow.png")

path = [
    (-49, 400),
    (800, 400),
    (800, 150),
    (525, 150),
    (525, 815),
    (250, 815),
    (250, 575),
    (1025, 575),
    (1050, 315),
    (1235, 315),
    (1220, 730),
    (730, 740),
    (730, 1080),
]

class RedBloon:
    def __init__(self, image_path, x, y, speed, path):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.speed = speed
        self.path = path
        self.current_point = 0 

    def follow_path(self):
        if self.current_point >= len(self.path):
            return

        target_x, target_y = self.path[self.current_point]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            self.x, self.y = target_x, target_y
            self.current_point += 1
        else:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

# Start at the first path point
start_x, start_y = path[0]
bloon = RedBloon("images/bloons/redbloon.png", start_x, start_y, speed=2, path=path)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    bloon.follow_path()

    screen.blit(map, (0, 0))
    bloon.draw(screen)

    pygame.draw.rect(screen, darkbrown, pygame.Rect(1673, -10, 260, 1100).inflate(5 * 2, 5 * 2), border_radius=35)

    pygame.draw.rect(screen, brown, pygame.Rect(1673, -10, 260, 1100), border_radius=30)

    pygame.display.update()
    clock.tick(60)
