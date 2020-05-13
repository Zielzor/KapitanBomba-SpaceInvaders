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

# wczytywanie grafik stateczków
red_space_ship = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
green_space_ship = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
blue_space_ship = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))
# protagonista tego filmu drogi
yellow_space_ship = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

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
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 35)
        
    player_velocity = 5 

    ship = Ship(300, 530)

    clock = pygame.time.Clock()

    

    def redraw_window():
        WINDOW.blit(back_ground, (0, 0))
        # draw text
        label_lives = main_font.render(f"LIVES: {lives}", 1, (255, 255, 255))
        label_level = main_font.render(f"LEVEL: {level}", 1, (255, 255, 255))
        WINDOW.blit(label_lives, (10, 10))
        WINDOW.blit(label_level, (WIDTH - label_level.get_width() - 10, 10))
        
        ship.draw(WINDOW)

        pygame.display.update()

    while run:
        clock.tick(FPS)  # sprawdzenia ciągłości 60xminute
        redraw_window()

        for event in pygame.event.get():  # sprwadzenie eventow i regowanie jezeli wystapiły
            if event.type == pygame.QUIT:  # raczej zrozumiale, jeżeli  zamkniemy okno, gra sie konczy
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and ship.x - player_velocity > 0 : #w lewo
            ship.x -= player_velocity
        if keys[pygame.K_d] and ship.x + player_velocity < WIDTH : #w prawo 
            ship.x += player_velocity
        if keys[pygame.K_w] and ship.y - player_velocity > 0 : # do góry
            ship.y -= player_velocity
        if keys[pygame.K_s] and ship.y + player_velocity < HEIGHT : # w dół
            ship.y += player_velocity

main()  # zamkniecie głównej petli

# https://youtu.be/Q-__8Xw9KTM?t=2626
# dodanie postaci i implementacja poruszania się, next step
