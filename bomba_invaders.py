import pygame
import os
import time
import random
pygame.init()
pygame.font.init()

# setting up window
WIDTH, HEIGHT = 640, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kapitan Bomba - Ciu Ciu Laserkami")

# laoding assets

# wczytywanie grafik stateczków wrogów
red_space_ship = pygame.image.load(
    os.path.join("assets", r"pixel_ship_red_small.png"))
green_space_ship = pygame.image.load(
    os.path.join("assets", r"pixel_ship_green_small.png"))
blue_space_ship = pygame.image.load(
    os.path.join("assets", r"pixel_ship_blue_small.png"))
# protagonista tego filmu drogi
yellow_space_ship = pygame.image.load(
    os.path.join("assets", r"pixel_ship_yellow.png"))

# background assets & other stuff

# ciu ciu laserki
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

# laserek protagonisty
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))

# tło
back_ground = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# definiowanie głownej petli i założeń


class Ship:
    """klasa abstrakcyjna służąca do dziedziczenia, bo mamy nasz statek i statki kosmitów"""
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        WINDOW.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
                "red" : (red_space_ship, red_laser),
                "green" : (green_space_ship, green_laser),
                "blue" : (blue_space_shipm blue_laser),
    }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel #tylko y wrogowie poruszają się z goóry na dół

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 35)
        
    player_velocity = 5 

    player = Player(300, 530)

    clock = pygame.time.Clock()

    

    def redraw_window():
        WINDOW.blit(back_ground, (0, 0))
        # draw text
        label_lives = main_font.render(f"LIVES: {lives}", 1, (255, 255, 255))
        label_level = main_font.render(f"LEVEL: {level}", 1, (255, 255, 255))
        WINDOW.blit(label_lives, (10, 10))
        WINDOW.blit(label_level, (WIDTH - label_level.get_width() - 10, 10))
        
        player.draw(WINDOW)

        pygame.display.update()

    while run:
        clock.tick(FPS)  # sprawdzenia ciągłości 60xminute
        redraw_window()

        for event in pygame.event.get():  # sprwadzenie eventow i regowanie jezeli wystapiły
            if event.type == pygame.QUIT:  # raczej zrozumiale, jeżeli  zamkniemy okno, gra sie konczy
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: #w lewo
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: #w prawo 
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: # do góry
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT: # w dół
            player.y += player_velocity

main()  # zamkniecie głównej petli


# nastepnie: spawnowanie sie statkow, poruszanie sie i laserki


# dodanie postaci i implementacja poruszania się, next step

