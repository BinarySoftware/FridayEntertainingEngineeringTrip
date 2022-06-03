import pygame

pygame.init()
win = pygame.display.set_mode((1100, 700))
pygame.display.set_caption("FEET")

x = 0
y = 40
szerokosc = 20
wysokosc = 20
krok = 20
run = True

while run:
    # opóźnienie w grze
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # obsługa zdarzeń 
    keys = pygame.key.get_pressed()
    # warunki do zmiany pozycji obiektu
    if keys[pygame.K_LEFT]:
        x -= krok
    if keys[pygame.K_RIGHT]:
        x += krok
    if keys[pygame.K_UP]:
        y -= krok
    if keys[pygame.K_DOWN] :
        y += krok
    # "czyszczenie" ekranu
    win.fill((0, 0, 0))
    # rysowanie prostokąta
    pygame.draw.rect(win, (0, 255, 0), (x, y, szerokosc, wysokosc))
    # odświeżenie ekranu 
    pygame.display.update()
