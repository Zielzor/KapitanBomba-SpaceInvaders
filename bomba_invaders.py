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
    os.path.join("assets_bomba", r"orzel_1_player.png"))

# background assets & other stuff

# ciu ciu laserki
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

# laserek protagonisty
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# tło
back_ground = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# definiowanie głownej petli i założeń

class Laser:
    def __init__(self, x, y, img):
        self.x = x 
        self.y = y 
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        WINDOW.blit(self.img, (self.x, self.y) )

    def move(self, vel):
        self.y += vel 

    def off_screen(self,height):
        return not (self.y <= height and self.y >= 0)  

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    """klasa abstrakcyjna służąca do dziedziczenia, bo mamy nasz statek i statki kosmitów"""
    COOLDOWN = 30 # 0,5 sekundy bo 60fps 
    
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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10 
                self.lasers.remove(laser) 

    def get_width(self):
        return self.ship_img.get_width()
   
    def get_height(self):
        return self.ship_img.get_height()
   
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0 
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

   
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 35, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers: 
                            self.lasers.remove(laser)
    
    def draw(self,window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self,window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(),10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health) ,10))

class Enemy(Ship):
    COLOR_MAP = {
                "red" : (red_space_ship, red_laser),
                "green" : (green_space_ship, green_laser),
                "blue" : (blue_space_ship, blue_laser)
    }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel #tylko y wrogowie poruszają się z goóry na dół
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



def collide(obj1,obj2):#collide jest poza klasą ship
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None    

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    
    main_font = pygame.font.SysFont("comicsans", 35)
    lost_font = pygame.font.SysFont("comicsans", 45)

    enemies = [] 
    wave_lenght = 5
    enemy_vel =  1 
        
    player_velocity = 5
    laser_velocity = 6 

    player = Player(300, 530)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0    

    def redraw_window():
        WINDOW.blit(back_ground, (0, 0))
        # draw text
        label_lives = main_font.render(f"LIVES: {lives}", 1, (255, 255, 255))
        label_level = main_font.render(f"LEVEL: {level}", 1, (255, 255, 255))
        WINDOW.blit(label_lives, (10, 10))
        WINDOW.blit(label_level, (WIDTH - label_level.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("DEFECATED", 1 , (255,255,255))
            WINDOW.blit(lost_label,(WIDTH/2 - lost_label.get_width()/2,320))

        pygame.display.update()

    while run:
        clock.tick(FPS)  # sprawdzenia ciągłości 60xminute
        redraw_window() 
        if lives <= 0 or player.health <=0:
            lost = True
            lost_count += 1

        if lost: #jeżeli lost = true
            if lost_count > FPS * 3 :
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_lenght += 5 
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-150,-100), random.choice(["red","blue","green"]))
                enemies.append(enemy)

        

        for event in pygame.event.get():  # sprwadzenie eventow i regowanie jezeli wystapiły
            if event.type == pygame.QUIT:  # raczej zrozumiale, jeżeli  zamkniemy okno, gra sie konczy
                run = False
#sterowaneko
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: #w lewo
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: #w prawo 
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: # do góry
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 10 < HEIGHT: # w dół
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
#zachowanie kosmitów
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_velocity,player)

            if random.randrange(0, 4*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            


        player.move_lasers(-laser_velocity, enemies)  

def menu():
    menu_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WINDOW.blit(back_ground,(0,0))
        menu_label = menu_font.render("Myk kursorkiem to start...", 1, (255,255,255))
        WINDOW.blit(menu_label, (WIDTH/2 - menu_label.get_width()/2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

menu()  # zamkniecie głównej petli


#nastepnie: dodanie kolizji i laserów  




