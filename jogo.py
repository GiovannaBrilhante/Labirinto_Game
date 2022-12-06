# Simple pygame program
# Import and initialize the pygame library
import pygame
import random
import os

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

SPRITESHEET_LOGO = 'abertura.png'



# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Define a Player object by extending pygame.sprite.Sprite
#The surface drawn on the screen is now an attribute of 'player'

class Player(pygame.sprite.Sprite):
    def __init__(self):
       super(Player, self).__init__()
       self.surf = pygame.image.load("assets/sergio.jpg").convert()
       self.surf.set_colorkey((255,255,255), RLEACCEL)
       self.rect= self.surf.get_rect()
       self.rect.x = 0
       self.rect.y = SCREEN_HEIGHT / 2
       self.speed = 3
       
           # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

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

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'

class Parede(pygame.sprite.Sprite):
    def __init__(self, config, cor):
        super(Parede, self).__init__()
        print("Parede X ",config[0],"Y ",config[1],"Larg ",config[2],"Alt ",config[3])
        print("Parede: " ,(config[2], config[3]), " Cor:" , cor)
        self.surf = pygame.Surface((config[2], config[3]))
        self.surf.fill(cor)
        self.rect = self.surf.get_rect()
        self.rect.x = config[0]
        self.rect.y = config[1]

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
           self.kill()
     
     
    def carregar_arquivos(self):
         diretorio_imagens= os.path.join(os.getcwd(),'assets')
         self.spritesheet = os.path.join(diretorio_imagens,SPRITESHEET_LOGO)
         self.spritesheet = pygame.image.load(self.spritesheet).convert()
         
          
azul = (0, 0, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
rosa = (235, 0, 251)
paredes_conf = [                  #                   sreem, cor(rgb), [rect.x,rect.y,larg, altura]       
    [[400, 200, 200, 200], azul], # pygame.draw.rect(screen, (0, 0, 255), [400, 400, 200, 200])      
    [[200, 400, 200, 200], verde],
    [[200, 300, 200, 100], verde],
    [[200, 000, 200, 100], verde],
    [[600, 400, 200, 200], vermelho],
    [[600, 300, 200, 100], vermelho],
    [[600, 000, 200, 100], vermelho],
    [[700, 000, 100, 200], vermelho],
    [[700, 200, 100, 100], (0, 0,0)],
    [[000, 400, 200, 200],  rosa],
    [[000, 000, 200, 200],  rosa]
]

paredes = pygame.sprite.Group()
# Adiciona paredes ao grupo
for parede_conf in paredes_conf:
    print("ParedeConf1: ", parede_conf[0], "ParedeCor: ",parede_conf[1])
    parede = Parede(parede_conf[0], parede_conf[1])
    paredes.add(parede)

FPS = 60
clock = pygame.time.Clock()
running = True
while running:

 # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:

            if event.type == K_ESCAPE:
                running = False

        # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    enemies.update()
 # Fill the background with white
    screen.fill((255, 255, 255))
    # parede = Parede(paredes_conf, paredes_conf[4])
    # screen.blit(parede.surf, parede.rect)
    #for parede_conf in paredes_conf:
     #   parede = Parede(parede_conf[0], parede_conf[1])

    # Exibe as paredes
    for parede in paredes:
        screen.blit(parede.surf, parede.rect)

    if pygame.sprite.spritecollideany(player, paredes):
        player.kill()
        running = False
    '''
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
'''
    screen.blit(player.surf, player.rect)
    for entity in all_sprites:
          screen.blit(entity.surf, entity.rect)



    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running = False

 # Flip the display
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
