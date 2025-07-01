import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Bloons TD 6')
clock = pygame.time.Clock()

font = pygame.font.Font("LuckiestGuy-Regular.ttf", 60)

overlay = pygame.Surface((108, 140), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 50))

# Colors
brown = (193,152,95)
brown2 = (148, 99, 54)
brown3 = (159, 120, 67)
darkbrown = (122,92,59)
darkbrown2 = (136, 89, 48)
darkbrown3 = (151, 112, 61)
white = (255, 255, 255)
black = (0, 0, 0)

tower_selected = ""
place_tower = ""
just_bought = "False"

# Load background
map = pygame.image.load("images/maps/MonkeyMeadow.png")

upgradebefore = pygame.image.load("images/gameui/upgrades.png")
upgrades = pygame.transform.scale(upgradebefore, (211, 74))

DartMonkeyShopbefore = pygame.image.load("images/gameui/DartMonkeyShop.png")
DartMonkeyShop = pygame.transform.scale(DartMonkeyShopbefore, (108, 140))
DartMonkeyShopSelectbefore = pygame.image.load("images/gameui/DartMonkeyShopSelect.png")
DartMonkeyShopSelect = pygame.transform.scale(DartMonkeyShopSelectbefore, (108, 140))
DartMonkeyShop_rect = pygame.Rect(1799, 170, 108, 140)
DartMonkeybefore = pygame.image.load("images/towers/DartMonkey.png")
DartMonkey = pygame.transform.scale(DartMonkeybefore, (97, 129))
RedDartMonkeybefore = pygame.image.load("images/towers/RedDartMonkey.png")
RedDartMonkey = pygame.transform.scale(RedDartMonkeybefore, (112, 133))
PlaceDartMonkeybefore = pygame.image.load("images/towers/PlaceDartMonkey.png")
PlaceDartMonkey = pygame.transform.scale(PlaceDartMonkeybefore, (104, 134))

circle_surf = pygame.Surface((70, 70), pygame.SRCALPHA)  # 35 * 2
pygame.draw.circle(circle_surf, (255, 0, 0, 80), (35, 35), 35)

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
    (820, 275),
    (800, 150),
    (525, 150),
    (530, 790),
    (380, 825),
    (250, 790),
    (250, 575),
    (930, 575),
    (1030, 535),
    (1050, 315),
    (1235, 315),
    (1250, 520),
    (1220, 730),
    (730, 740),
    (715, 1080),
]

def get_hitbox(mousex, mousey, tower):
    if tower == "Dart Monkey":
        return pygame.Rect(mousex - 97 / 3.2, mousey - 129 / 8, 97 / 1.6, 129 / 2.1)

def get_path_block_points(path, radius, spacing=15):
    block_points = []

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        steps = max(1, int(distance / spacing))

        for step in range(steps + 1):
            t = step / steps
            x = x1 + dx * t
            y = y1 + dy * t
            block_points.append((x + 35, y + 35))

    return block_points

def is_touching_block_zone(mouse_pos, block_zones, towers, block_width=60, block_height=60, tower_width=60, tower_height=60):
    new_rect = get_hitbox(mouse_pos[0], mouse_pos[1], place_tower)

    # Check collision with block zones (assuming block_zones is list of (x, y) centers)
    for x, y in block_zones:
        block_rect = pygame.Rect(
            x - block_width // 2 - 15,
            y - block_height // 2 + 20,
            block_width,
            block_height
        )
        if new_rect.colliderect(block_rect):
            return True

    # Check collision with other towers
    for tower in towers:
        if tower.hitbox.get_rect().colliderect(new_rect):
            return True

    return False


block_zones = get_path_block_points(path, radius=35, spacing=15)

class Hitbox:
    def __init__(self, x, y, width, height, name):
        # x and y represent the center
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

    def get_rect(self):
        return get_hitbox(self.x, self.y, self.name)

    def is_colliding(self, other_rect):
        return self.get_rect().colliderect(other_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 2)

class Tower:
    def __init__(self, name, x, y, image_path, width, height, towerID, range_radius=100):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.range_radius = range_radius
        self.selected = False
        self.id = towerID
        self.hitbox = Hitbox(x, y, width, height, name)

    def draw(self, surface):
        # Draw range circle if selected
        if self.selected:
            pygame.draw.circle(surface, (0, 255, 0, 60), (self.x, self.y), self.range_radius, width=2)

        # Draw tower image
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def set_selected(self, state):
        self.selected = state

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
bloons = [RedBloon("images/bloons/redbloon.png", start_x, start_y, speed=2, path=path)]
towers = []

# Main game loop
while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not place_tower == "":
                if not is_touching_block_zone(mouse_pos, block_zones, towers):
                    if mouse_pos[0] < 1670 and place_tower == "Dart Monkey":
                        towers.append(Tower("Dart Monkey", mouse_pos[0], mouse_pos[1], "images/towers/DartMonkey.png", 97, 129, len(towers), 100))
                    place_tower = ""
            if just_bought: 
                just_bought = False
            if DartMonkeyShop_rect.collidepoint(event.pos):
                tower_selected = "Dart Monkey"
                just_bought = True
    
    screen.blit(map, (0, 0))

    for bloon in bloons:
        bloon.follow_path()
        bloon.draw(screen)

    for tower in sorted(towers, key=lambda t: t.y):
        tower.draw(screen)
        tower.hitbox.draw(screen)
        

    pygame.draw.rect(screen, darkbrown, pygame.Rect(1673, -10, 260, 1100).inflate(5 * 2, 5 * 2), border_radius=35)

    pygame.draw.rect(screen, brown, pygame.Rect(1673, -10, 260, 1100), border_radius=30)

    screen.blit(upgrades, (1695, 10))

    pygame.draw.polygon(screen, darkbrown2, get_cut_corner_rect_points(1685, 95, 220, 60, 5))
    pygame.draw.polygon(screen, brown2, get_cut_corner_rect_points(1695, 105, 200, 40, 5))
    
    font = pygame.font.Font("LuckiestGuy-Regular.ttf", 25)
    screen.blit(font.render(tower_selected, True, (255, 255, 255)), (1720, 115))

    pygame.draw.polygon(screen, darkbrown3, get_cut_corner_rect_points(1680, 166, 232, 750, 8))
    pygame.draw.rect(screen, brown3, pygame.Rect(1686, 172, 220, 738))

    screen.blit(DartMonkeyShop, (1685, 170))

    # for x, y in block_zones:
    #     screen.blit(circle_surf, (x - 35 - 15, y - 35 + 20))

    if tower_selected == "Dart Monkey":
        screen.blit(DartMonkeyShopSelect, (1801, 171))
    else:
        if DartMonkeyShop_rect.collidepoint(mouse_pos):
            screen.blit(DartMonkeyShop, (1799, 170))
            screen.blit(overlay, (1799, 170))
        else: 
            screen.blit(DartMonkeyShop, (1799, 170))

    if just_bought and mouse_pos[0] < 1677:
        place_tower = tower_selected
        just_bought = False
    
    if place_tower != "":
        if mouse_pos[0] > 1677 or mouse_pos[0] < 1 or mouse_pos[1] < 1 or mouse_pos[1] > 1078:
            place_tower = ""
        
        if place_tower == "Dart Monkey":
            if is_touching_block_zone(mouse_pos, block_zones, towers):
                screen.blit(RedDartMonkey, (mouse_pos[0] - DartMonkey.get_width() / 2, mouse_pos[1] - DartMonkey.get_height() / 2))
            else:
                screen.blit(PlaceDartMonkey, (mouse_pos[0] - DartMonkey.get_width() / 2, mouse_pos[1] - DartMonkey.get_height() / 2))
    
    # print(mouse_pos)


    pygame.display.update()
    clock.tick(60)