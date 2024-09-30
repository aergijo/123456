import pygame
import sys
import random

pygame.init()

window_size = (640, 480)
PLAYERCOLOR = [0,0,0]
enemynumber = 2

background_image = pygame.image.load('russha.png')
background_image = pygame.transform.scale(background_image, window_size)

screen = pygame.display.set_mode(window_size)

pygame.display.set_caption("стрелялка")

class Enemy(pygame.Rect):
    def __init__(self,x):
        super().__init__(x,0,25,25)
        self.speed = 1
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color_change_time = pygame.time.get_ticks()
    def move(self):
        self.y += self.speed
        if self.y >= 420:
            pygame.quit()
            sys.exit()
    def draw(self,screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.color_change_time > 10: 
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.color_change_time = current_time
        pygame.draw.rect(screen,self.color,self)
    

class Bullet1(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 15, 10)  
        self.speed =  10

    def move(self):
        self.y -= self.speed
        for i in range(len(enemies)):
            if self.colliderect(enemies[i]):
                enemies.pop(i)
                break
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self) 

class Player(pygame.Rect):
    def __init__(self):
        super().__init__(100, 400, 25, 25) 
        self.speed = 15

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.x >= 0:
                self.x -= self.speed
        if keys[pygame.K_d]:
            if self.x <= window_size[0]-25:
                self.x += self.speed
        for i in range(len(enemies)):
            if self.colliderect(enemies[i]):
                pygame.quit()
                sys.exit()
    def draw(self, screen):
        pygame.draw.rect(screen, PLAYERCOLOR, self) 

bullets = []
enemies = []
player = Player()
FPS = 50

def spawnEnemy():
    if len(enemies) < enemynumber:
        enemy = Enemy(random.randint(0,640))
        enemies.append(enemy)
    for i in enemies:
        i.move()
        i.draw(screen)

clock = pygame.time.Clock()

def spawnbullet1(): 
    bullet = Bullet1(player.centerx, player.top)
    bullets.append(bullet)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       #if event.type == pygame.MOUSEBUTTONDOWN:
        #    if event.button == 1:
         #       spawnbullet1()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                spawnbullet1()


    player.move()
    for bullet in bullets:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)


    #screen.fill((255, 255, 255)) 
    screen.blit(background_image, (0, 0))  

    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    spawnEnemy()


    
    pygame.display.flip()
    clock.tick(FPS)