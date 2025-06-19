import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Bloons TD 6')
clock = pygame.time.Clock()

font = pygame.font.Font("LuckiestGuy-Regular.ttf", 60)

# Colors
brown = (193,152,95)
brown2 = (148, 99, 54)
brown3 = (159, 120, 67)
darkbrown = (122,92,59)
darkbrown2 = (136, 89, 48)
darkbrown3 = (151, 112, 61)
white = (255, 255, 255)
black = (0, 0, 0)

# Load background
map = pygame.image.load("images/maps/MonkeyMeadow.png")

upgradebefore = pygame.image.load("images/gameui/upgrades.png")
upgrades = pygame.transform.scale(upgradebefore, (211, 74))

DartMonkeyShopbefore = pygame.image.load("images/gameui/DartMonkeyShop.png")
DartMonkeyShop = pygame.transform.scale(DartMonkeyShopbefore, (108, 140))

def get_cut_corner_rect_points(x, y, w, h, cut):
    return [
        (x + cut, y),
        (x + w - cut, y),
        (x + w, y + cut),
        (x + w, y + h - cut),
        (x + w - cut, y + h),
        (x + cut, y + h),
        (x, y + h - cut),
        (x, y + cut),
    ]

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

    screen.blit(upgrades, (1695, 10))

    pygame.draw.polygon(screen, darkbrown2, get_cut_corner_rect_points(1685, 95, 220, 60, 5))
    pygame.draw.polygon(screen, brown2, get_cut_corner_rect_points(1695, 105, 200, 40, 5))

    pygame.draw.polygon(screen, darkbrown3, get_cut_corner_rect_points(1680, 166, 232, 750, 8))
    pygame.draw.rect(screen, brown3, pygame.Rect(1686, 172, 220, 738))

    screen.blit(DartMonkeyShop, (1685, 170))
    screen.blit(DartMonkeyShop, (1799, 170))

    


    pygame.display.update()
    clock.tick(60)
