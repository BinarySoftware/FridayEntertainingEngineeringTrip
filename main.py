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
IS_DEADLY_BORDER = True

x = pygame.display.get_window_size()[0]/2
y = pygame.display.get_window_size()[1]/2
food_x = random.randint(100, pygame.display.get_window_size()[0]-100)
food_y = random.randint(100, pygame.display.get_window_size()[1]-100)
special_food_x = random.randint(100, pygame.display.get_window_size()[0]-100)
special_food_y = random.randint(100, pygame.display.get_window_size()[1]-100)

special_food = None
food = None
player = None
border = None
inner = None
hud = None

score = 0
length = 3
delay = 150
last_positions = [(x, y)]

direction = 0 # 0-u, 1-r, 2-b, 3-l

font = pygame.font.SysFont('Avenir Next', 24)

t1 = time.time()

while RUN:
    keys = pygame.key.get_pressed()
    pygame.time.delay(delay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    if IS_ALIVE:
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and direction != 1:
            direction = 3
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and direction != 3:
            direction = 1
        if keys[pygame.K_w] or keys[pygame.K_UP] and direction != 2:
            direction = 0
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and direction != 0:
            direction = 2

        if direction == 0:
            y -= STEP
        elif direction == 1:
            x += STEP
        elif direction == 2:
            y += STEP
        elif direction == 3:
            x -= STEP

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
            if delay > 50:
                delay -= 10
            IS_FOOD = True

        t2 = time.time()

        if not IS_SPECIAL_FOOD and t2 - t1 > 10:
            IS_SPECIAL_FOOD = True
            special_food_x = random.randint(100, pygame.display.get_window_size()[0]-100)
            special_food_y = random.randint(100, pygame.display.get_window_size()[1]-100)
            t1 = t2

        WINDOW.fill((0, 0, 0))

        if IS_DEADLY_BORDER:
            border = pygame.draw.rect(WINDOW, (0, 0, 255), (0, 0, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))
            inner = pygame.draw.rect(WINDOW, (25, 25, 25), (WIDTH+0.5*WIDTH, WIDTH+0.5*WIDTH, 
                                                            pygame.display.get_window_size()[0]-3*(WIDTH+1),
                                                            pygame.display.get_window_size()[1]-3*(WIDTH+1)))

        hud = font.render(f'Score: {score}', False, (250, 250, 250))
        WINDOW.blit(hud, (15,15))

        if IS_SPECIAL_FOOD:
            if t2-t1 > 4:
                IS_SPECIAL_FOOD = False
                t1 = t2
            special_food = pygame.draw.rect(WINDOW, (255, 255, 0), (special_food_x, special_food_y, WIDTH, HEIGHT))

        food = pygame.draw.rect(WINDOW, (255, 0, 0), (food_x, food_y, WIDTH, HEIGHT))
        player = pygame.draw.rect(WINDOW, (0, 250, 0), (x, y, WIDTH, HEIGHT))

        for i in range(len(last_positions)-1):
            col = 100*i/len(last_positions)
            body_part = pygame.draw.rect(WINDOW, (0, 100+col, 0), (last_positions[i][0], last_positions[i][1], WIDTH-2, HEIGHT-2))
            if player.colliderect(body_part):
                 IS_ALIVE = False

        if player.colliderect(food):
            IS_FOOD = False

        if special_food and player.colliderect(special_food):
            IS_SPECIAL_FOOD = False
            score += 100
            length += 1

        if IS_DEADLY_BORDER and player.colliderect(border) and not player.colliderect(inner):
            IS_ALIVE = False

    if not IS_ALIVE:
        WINDOW.fill((255, 255, 255))
        hud = font.render(f'YOU LOST WITH SCORE: {score}. BUT THE GRIND SHALL NEVER STOP!', False, (0, 0, 0))
        hud2 = font.render('Press Cmd+Q or Alt+F4 to quit.', False, (0, 0, 0))
        WINDOW.blit(hud, (pygame.display.get_window_size()[0]/2-350,pygame.display.get_window_size()[1]/2-50))
        WINDOW.blit(hud2, (pygame.display.get_window_size()[0]/2-150,pygame.display.get_window_size()[1]/2+50))

    pygame.display.update()
