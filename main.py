import random
import pygame
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.png")

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo-flying.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("battleship.png")
playerX = 368
playerY = 480
playerX_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Background
mixer.music.load("imperial_march.wav")
mixer.music.play(-1)

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("pixelated-alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
bullet_img = pygame.image.load("laser.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over code
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    if distance <= 30:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (-125, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("blaster-firing.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] >= 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            enemyX[i] = 0
        elif enemyX[i] > 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            enemyX[i] = 736
        # collision
        coll = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if coll:
            if enemyY[i] < 450:
                bulletY = 480
                bullet_state = 'ready'
                score_value += 10
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bullet_state = 'ready'
        bulletY = 480

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
