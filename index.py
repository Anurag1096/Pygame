import random
import sys
import math
import pygame
from pygame import mixer

# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("spba.png")
# Background sounds
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space doom")
icon = pygame.image.load("spac.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("spla.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

# Bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
# Ready state no bullet
# Fire state moving bullet
bullet_state = "ready"

# scoring system
score_value = 0
font = pygame.font.Font('Oh My Baby.ttf', 32)
textX = 10
textY = 10
# Game over text
game_font = pygame.font.Font('Oh My Baby.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 234, 245))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_font.render("GAME OVER ", True, (255, 234, 245))
    screen.blit(over_text, (200, 250))


# Creating the function for player


def player(x, y):
    screen.blit(playerimg, (x, y))


# Creating the function for enemy


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# Creating the bullet movement


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# creating the bullet colision


def isCollosion(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        "# if keystroke is pressed"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_UP:
                playerY_change -= 5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Setting the boundary of the player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # setting the vertical boundary
    playerY += playerY_change

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Setting the boundary of the enemy
    for i in range(num_of_enemies):

        # Game over

        if enemyY[i] >= 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # bullet collision
        collision = isCollosion(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the player function
    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
sys.exit()
