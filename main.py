from cProfile import run
import pygame
import random
import time

pygame.init()
pygame.font.init()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# WINDOW = pygame.display.set_mode((400, 400))
pygame.display.set_caption("FEET")

WIDTH = pygame.display.get_window_size()[0]/40
HEIGHT = pygame.display.get_window_size()[0]/40
STEP = pygame.display.get_window_size()[0]/40

RUN = True
IS_ALIVE = True
IS_FOOD = True
IS_SPECIAL_FOOD = False
IS_DEADLY_BORDER = False

x = pygame.display.get_window_size()[0]/2
y = pygame.display.get_window_size()[1]/2
food_x = random.randint(100, pygame.display.get_window_size()[0]-100)
food_y = random.randint(100, pygame.display.get_window_size()[1]-100)

food = None
player = None
border = None
inner = None

score = 0
length = 3
last_positions = [(x, y)]

font = pygame.font.SysFont('Avenir Next', 24)

while RUN:
    pygame.time.delay(100)
    if IS_ALIVE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            x -= STEP
        if keys[pygame.K_d]:
            x += STEP
        if keys[pygame.K_w]:
            y -= STEP
        if keys[pygame.K_s] :
            y += STEP

        if not IS_DEADLY_BORDER:
            if x > pygame.display.get_window_size()[0]:
                x = 0
            if x < 0:
                x = pygame.display.get_window_size()[0]
            if y > pygame.display.get_window_size()[1]:
                y = 0
            if y < 0:
                y = pygame.display.get_window_size()[1]
        
        last_positions.append((x, y))
        if len(last_positions) > length:
            last_positions.pop(0)

        if not IS_FOOD:
            food_x = random.randint(100, pygame.display.get_window_size()[0]-100)
            food_y = random.randint(100, pygame.display.get_window_size()[1]-100)
            score += 10
            length += 1
            IS_FOOD = True

        WINDOW.fill((0, 0, 0))
        if IS_DEADLY_BORDER:
            border = pygame.draw.rect(WINDOW, (0, 0, 255), (0, 0, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))
            inner = pygame.draw.rect(WINDOW, (25, 25, 25), (WIDTH+0.5*WIDTH, WIDTH+0.5*WIDTH, 
                                                            pygame.display.get_window_size()[0]-3*(WIDTH+1),
                                                            pygame.display.get_window_size()[1]-3*(WIDTH+1)))

        hud = font.render(f'Score: {score}', False, (250, 250, 250))
        WINDOW.blit(hud, (15,15))
        food = pygame.draw.rect(WINDOW, (255, 0, 0), (food_x, food_y, WIDTH, HEIGHT))
        for pos in last_positions:
            pygame.draw.rect(WINDOW, (0, 200, 0), (pos[0], pos[1], WIDTH-2, HEIGHT-2))
        player = pygame.draw.rect(WINDOW, (0, 250, 0), (x, y, WIDTH, HEIGHT))

        if player.colliderect(food):
            IS_FOOD = False

        if IS_DEADLY_BORDER and player.colliderect(border) and not player.colliderect(inner):
            hud = font.render(f'YOU LOST WITH SCORE: {score}. BUT THE GRIND SHALL NEVER STOP!', False, (250, 250, 250))
            WINDOW.blit(hud, (pygame.display.get_window_size()[0]/2-350,pygame.display.get_window_size()[1]/2))
            IS_ALIVE = False

    pygame.display.update()
