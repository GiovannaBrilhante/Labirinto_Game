# Simple pygame program
# Import and initialize the pygame library
import pygame

import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Run until the user asks to quit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/sergio.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(30, 30))

    # Move the sprite based on user keypresses

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
                self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
                self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:

 # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
     
           if event.type == K_ESCAPE:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #Update the player sprite based on user keypresses
    player.update(pressed_keys)
 # Fill the background with white
    screen.fill((255, 255, 255))

# pygame.draw.rect(screen, cor rgb, [posX, posY, largura, altura])
# indo de 200 em 200
    # azul
    pygame.draw.rect(screen, (0, 0, 255), [400, 200, 200, 200])
    pygame.draw.rect(screen, (0, 0, 255), [400, 400, 200, 200])
    # verde
    pygame.draw.rect(screen, (0, 255, 0), [200, 400, 200, 200])
    pygame.draw.rect(screen, (0, 255, 0), [200, 300, 200, 100])
    pygame.draw.rect(screen, (0, 255, 0), [200, 000, 200, 100])
    # vermelho
    pygame.draw.rect(screen, (255, 0, 0), [600, 400, 200, 200])
    pygame.draw.rect(screen, (255, 0, 0), [600, 300, 200, 100])
    pygame.draw.rect(screen, (255, 0, 0), [600, 000, 200, 100])
    pygame.draw.rect(screen, (255, 0, 0), [700, 000, 100, 200])
    # saida
    #pygame.draw.rect(screen, (0, 0,0), [700, 200, 100, 100])
    # rosa
    pygame.draw.rect(screen, (235, 0, 251), [000, 400, 200, 200])
    pygame.draw.rect(screen, (235, 0, 251), [000, 000, 200, 200])


# Flip the display
    pygame.display.flip()




pygame.quit()
