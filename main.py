from math import e
import pygame
import random
from pygame import mixer

# initialize the pygame
pygame.init()
# create a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('./images/bg.jpg')

# background sound
mixer.music.load("./sounds/background.mp3")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./images/ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('./images/spaceship.png')
playerx = 370
playery = 500
playerx_change = 0
playery_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./images/alien.png'))
    enemyx.append(random.randint(50, 730))
    enemyy.append(random.randint(50, 350))
    enemyx_change.append(0.5)   #giving it 0.3 is super important
    enemyy_change.append(40)

# bullet
bulletImg = pygame.image.load('./images/bullet.png')
bulletx = 0
bullety = 500
bulletx_change = 0
bullety_change = 2
bullet_state = "ready"    # ready - you can't see the bullet on the screen

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)
over = False

def game_over_text():
    global over
    game_over = font.render("GAME OVER" ,True, (255,155,205))
    screen.blit(game_over, (320,300))
    over = True

def game_over_sound():
    if over == True:
        game_over_sound = mixer.Sound("./sounds/game_over.wav")
        game_over_sound.play()
    
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,155,205))
    screen.blit(score, (x,y))
    
def player(x,y):
    screen.blit(playerImg, (x,y))
    
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
    
def fire_bullet1(x,y):
    global bullet_state
    bullet_state = "fire"     #fire - bullet is currently moving
    screen.blit(bulletImg, (x-10, y + 10))
    
def fire_bullet2(x,y):
    global bullet_state
    bullet_state = "fire"     #fire - bullet is currently moving
    screen.blit(bulletImg, (x + 32 +10 , y + 10))

def iscollision(enemyx,enemyy,bulletx,bullety):
    distance = ((enemyx-bulletx)**2 + (enemyy-bullety)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

# game loop  
running = True
while running:
    # rgb = red, green, blue 0  - 255
    screen.fill((80, 50, 90))
    # background img
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #  if keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_LEFT:
            playerx_change = -0.7
        if event.key == pygame.K_RIGHT:
            playerx_change = 0.7
        # if event.key == pygame.K_UP:
        #     playery_change = -0.4
        # if event.key == pygame.K_DOWN:
        #     playery_change = 0.4
            
        if event.key == pygame.K_UP:
            if bullet_state is "ready":
                bullet_sound = mixer.Sound("./sounds/bullet_fire.wav")
                bullet_sound.play()
                # get the current x coordinate of the spaceship
                bulletx = playerx
                fire_bullet1(bulletx,bullety)
                fire_bullet2(bulletx,bullety)
            
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerx_change = 0  
        # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #     playery_change = 0   
   
    playerx += playerx_change
    playery += playery_change
    
    #checking for boundaries of spaceship so it doesn't go out of bounds
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
        
    # enemy movement  
    for i in range(num_of_enemies):
        # GAME OVER
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 1000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.3
            enemyy[i] += enemyy_change[i] 
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.3
            enemyy[i] += enemyy_change[i]
            
        # collision 
        collision1 = iscollision(enemyx[i],enemyy[i],playerx -10,bullety)
        collision2 = iscollision(enemyx[i],enemyy[i],playerx +42,bullety)
        if collision1:
            explosion_sound = mixer.Sound("./sounds/alien_explosion.wav")
            explosion_sound.play()
            bullety = 500
            bullet_state = "ready"   
            score_value += 1
            enemyx[i] = random.randint(50, 700)
            enemyy[i] = random.randint(50, 350)
            
        if collision2:
            explosion_sound = mixer.Sound("./sounds/alien_explosion.wav")
            explosion_sound.play()
            bullety = 500
            bullet_state = "ready"   
            score_value += 1
            enemyx[i] = random.randint(50, 700)
            enemyy[i] = random.randint(50, 350)
            
        enemy(enemyx[i] , enemyy[i], i)
    
    # bullet movement
    if bullety <= 0:
        bullety =500
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet1(bulletx,bullety)
        fire_bullet2(bulletx,bullety)
        bullety -= bullety_change
        
        
    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update()
    game_over_sound()
    