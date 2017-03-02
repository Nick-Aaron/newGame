import sys, pygame, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700
NEWFOOD = 100
foodCounter = 0
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('smile V0.5.1')
FOODSIZE = 60

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
SADDLEBROWN = (139, 69, 19)

player = pygame.Rect(300, 100, 50, 50)
foods = []
for i in range(10):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

playerImage = pygame.image.load('player.png')
playerStretchedImage = pygame.transform.scale(playerImage, (80, 80))
foodImage = pygame.image.load('face.png')
foodStretchedImage = pygame.transform.scale(foodImage, (FOODSIZE, FOODSIZE))
pickUpSound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('theMass.mp3')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 15

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = True
                moveRight = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = True
                moveUp = False
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
            if event.key == ord('x'):
                player = pygame.Rect(random.randint(0, WINDOWWIDTH - player.width), random.randint(0, WINDOWHEIGHT - player.height), player.width, player.height)
            if event.key == ord('m'):
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0] -30, event.pos[1] - 30, FOODSIZE, FOODSIZE))
    # move the player
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.bottom += MOVESPEED

    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 15, player.height + 15)
            playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
    # deaw the black background onto the surface
    windowSurface.fill(SADDLEBROWN)
    # draw the player onto the surface
    windowSurface.blit(playerStretchedImage, player)

    foodCounter += 1
    if foodCounter >= 40:
        # add new food
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

    # draw the food
    for food in foods[:]:
        windowSurface.blit(foodStretchedImage, food)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(30)