import pygame
from pygame.locals import *

def setting_size():
    pygame.init()

    screen = pygame.display.set_mode((500, 500), RESIZABLE)
    pygame.display.set_caption("Játék méretének beállítása")

    run = True
    while run:
        print(f"width: {screen.get_width()} height: {screen.get_height()}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

    return screen 