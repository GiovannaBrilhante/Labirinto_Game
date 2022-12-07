# Simple pygame program
# Import and initialize the pygame library
import pygame 


import gpiozero
import time

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

#Inicializando jogo
pygame.init()

#Definindo as portas do led

led = gpiozero.LED(19)
led2 = gpiozero.LED(28)
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



gameOver = False # variavel pra tela de gamer Over 
telaInicial = True #variavel pra tela de Abertura
ganhou = False   #Variavel pra mostrar se ganhou 
timer = 0
tempo_segundo = 0
font = pygame.font.Font("freesansbold.ttf", 20) #defina qual é a fonte e o tamanho
text = font.render("Tempo: ", True, (255, 255, 255), (0, 0, 0)) # defina qual mensagem e a cor do text
pos_texto = text.get_rect()
pos_texto.center = (45, 25) # DEFINIMOS A POSICAO ONDE O TEXTO CAI FICAR


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

#TAMANHO DA NOSSA TELA 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Serve pra pegar as mensagens e mostrar na tela 
def texto(msg, cor):
    fonte = font.render(msg, True, cor)
    screen.blit(fonte, [SCREEN_WIDTH/8, SCREEN_HEIGHT/2])

def text4(msg, cor):
    fonte = font.render(msg, True, cor)
    screen.blit(fonte, [250, SCREEN_HEIGHT/4])

def texto1(msg, cor):
    fonte = font.render(msg, True, cor)
    screen.blit(fonte, [50, SCREEN_HEIGHT/2])

def texto3(msg, cor):
    fonte = font.render(msg, True, cor)
    screen.blit(fonte, [SCREEN_WIDTH/4, SCREEN_HEIGHT/2 + 100])

def texto2(msg, cor):
    fonte = font.render(msg, True, cor)
    screen.blit(fonte, [SCREEN_WIDTH/8, SCREEN_HEIGHT/2])
# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


#Essa é a classe do Player(Jogador), onde definimos a imagem dele, na onde ele vai começar no 
# jogo e a sua velocidade
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/sergio.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT / 2
        self.speed = 3

   # os movimentos que o player pode fazer 
      
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

#aqui é uma variavel recebendo a classe Player
player = Player()


#Variavel recebendo o grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

  

# Aqui é a classe Parede,
# onde chama as configurações da parede.
#E o da  vitoria(QUE CASO O JOGADOR COLIDE)-> O JOGADOR GANHE


class Parede(pygame.sprite.Sprite):
    def __init__(self, config, cor,vitoria):
        super(Parede, self).__init__()
        print("Parede X ", config[0], "Y ", config[1],
              "Larg ", config[2], "Alt ", config[3])
        print("Parede: ", (config[2], config[3]), " Cor:", cor)
        self.surf = pygame.Surface((config[2], config[3]))
        self.surf.fill(cor)
        self.rect = self.surf.get_rect()
        self.rect.x = config[0]
        self.rect.y = config[1]
        self.vitoria = vitoria

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

  

# aqui as variaveis que definimos de suas cor. 
azul = (0, 0, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
rosa = (235, 0, 251)

# Esse parede_conf  serve para montar o nosso grupo de paredes, que são definidos 
# a posicao X, posicao Y , largura e altura e se ele é falso ou true

paredes_conf = [  # sreem, cor(rgb), [rect.x,rect.y,larg, altura]
    # pygame.draw.rect(screen, (0, 0, 255), [400, 400, 200, 200])
    [[400, 200, 200, 200], azul, False],
    [[400, 400, 200, 200], azul, False],
    [[200, 400, 200, 200], verde,False],
    [[200, 300, 200, 100], verde,False],
    [[200, 000, 200, 100], verde,False],
    [[600, 400, 200, 200], vermelho,False],
    [[600, 300, 200, 100], vermelho,False],
    [[600, 000, 200, 100], vermelho,False],
    [[700, 000, 100, 200], vermelho,False],
   [[700, 200, 100, 100], (0, 0, 0),True],
    [[000, 400, 200, 200],  rosa,False],
    [[000, 000, 200, 200],  rosa, False]
]
# colocamos se ele é False ou true -> Pra quando o jogador colidir numa  parede, caso ela bate numa parede que é True, quer dizer que ele chegou no destino e ganhou
# caso seja False, ele colidiu numa parede normal e ele perde o jogo

# variavel os grupo de sprites
vitorias = pygame.sprite.Group()
paredes = pygame.sprite.Group()

# Adiciona paredes ao grupo
for parede_conf in paredes_conf:
    
    print("ParedeConf1: ", parede_conf[0], "ParedeCor: ", parede_conf[1])
    parede = Parede(parede_conf[0], parede_conf[1], parede_conf[2])
    
    
    # nessa verificação, ele verifica que se a parede que colidiu é True quer dizer 
    # que ele ganhou, entao na variavel vitoria ele adiciona parede, caso entre no  False, ele colidiu na parede e nao ganhou
    if parede_conf[2] == True:
        vitorias.add(parede)
    else:
        paredes.add(parede)
 

FPS = 40
#Variavel que pega o tempo
clock = pygame.time.Clock()
#Variavel pra rodar o jogo
running = True
# o tempo do jogo
pygame.time.delay(50)

#Pra rodar o jogo
while running:
# caso o jogador ganhe
    while ganhou:
        #Mostra o Led acendendo 
        led.on()
        #o tempo que ele fica acesso
        time.sleep(1)
        # e apaga o led e por quando tempo fica apagado
        led.off()
        time.sleep(1)
        #E mostra mensagem que ele ganhou
        texto2(
            "O Sérgio foi levado até a portaria, você ganhou nota 10", (0, 0, 0))
        
        # pra quando ele sempre ganhar ir nessa tela 
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                # caso ele saia, o jogo sai e nao mostra que ele ganhou
                running = False
                ganhou = False
            if event.type == pygame.KEYDOWN:
                #opcao de apertar no TECLA B  pra rodar o jogo de novo -> QUER DIZER QUE ELE NAO GANHOU
                if event.key == pygame.K_b:
                    player.rect.x = 0
                    player.rect.y = SCREEN_HEIGHT / 2
                
                    running = True
                    ganhou= False
                    all_sprites.add(player)
                    timer = 0
                    #OPCAO BOTAO N pra ele sair do jogo
                if event.key == pygame.K_n:
                    
                    running = False
                    ganhou = False
                    
      # WHILE-> pra rodar a tela de gamer over 
      # caso ele perca, acende o led2('LED VERMELHO)
      # e por quando ele fica acesso e depois apaga e por quando tempo ele apaga              
    while gameOver:
        led2.on()
        time.sleep(1)
        led2.off()
        time.sleep(1)
        #mensagem pra mostrar caso ele perde  
        texto(
            "Game Over, para jogar novamente aperte a tecla B, ou N para sair", (0, 0, 0))
      #pra atualizar toda vez que ele perder entra nessa tela
        pygame.display.update()
      
      
        for event in pygame.event.get():
            if event.type == QUIT:
                # caso ele saia do jogo, o jogo para e nao mostra a tela de game over 
                running = False
                gameOver = False
            if event.type == pygame.KEYDOWN:
                # TECLA B -> pra ele reiniciar o jogo 
                if event.key == pygame.K_b:
                    player.rect.x = 0
                    player.rect.y = SCREEN_HEIGHT / 2
                    running = True
                    gameOver = False
                    all_sprites.add(player)
                    timer = 0
                    # TECLA N -> opcao pra ele sair do jogo
                if event.key == pygame.K_n:
                    running = False
                    gameOver = False

 # PRA QUANDO ELE FECHAR A TELA O JOGO NAO COMEÇAR
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.type == K_ESCAPE:
                running = False

# TELA DE ABERTURA -> ONDE MOSTRA OS TEXTOS E A COR E TODA QUE VEZ QUE ENTRAR NO JOGO MOSTRA A 
# TELA DE ABERTURA 
    while telaInicial:
        screen.fill((0, 255, 255))
        texto1("Pressione I para levar o Sérgio até a portaria do Cotuca(a caixa preta)", (255, 0, 0))
        texto3("Giovanna Brilhante e Geovana Oliveira", (255, 0, 0))
        text4("Labirinto no Cotuca", (255, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            # Evento para fechar o jogo
            if event.type == QUIT:
                running = False
                telaInicial = False
            if event.type == pygame.KEYDOWN:
                #TECLA I -> PRA COMEÇAR O JOGO
                if event.key == pygame.K_i:
                    running = True
                    telaInicial = False
                    all_sprites.add(player)
                    timer = 0
        # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

   
 # Fill the background with white
    screen.fill((255, 255, 255))
    
  #UM IF PRA VERIFICAO DE TEMPO
    if (timer < 20):
        timer += 1
    else:
        # AQUI MOSTRA O TEMPO QUE O JOGADOR ESTA JOGANDO
        tempo_segundo += 1
        text = font.render("Tempo: " + str(tempo_segundo),
                           True, (255, 255, 255), (0, 0, 0))
        timer = 0

    # Exibe as paredes
    for parede in paredes:
        screen.blit(parede.surf, parede.rect)

    for parede_vitoria in vitorias:
        screen.blit(parede_vitoria.surf, parede_vitoria.rect)


     
     # SE COLIDIR COM A PAREDE (PORTARIA), MOSTRA QUE ELE GANHOU
    if pygame.sprite.spritecollideany(player, vitorias):
        print(paredes)
        player.kill()
        ganhou = True

# SE COLIDIR COM  A PAREDE -> QUER DIZER QUE ELE MORREU E MOSTRA A TELA DE GAMER OVER
    if pygame.sprite.spritecollideany(player, paredes):
        print(paredes)
        player.kill()
        gameOver = True

    
     
  # AQUI SERIA VERSAO ANTES DAS  NOSSAS PAREDES.
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
    # MOSTRA NA TELA AS MENSAGENS, O PLAYER 
    screen.blit(text, pos_texto)
    screen.blit(player.surf, player.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

 # Flip the display
    pygame.display.flip()
    clock.tick(FPS)

#FECHA O JOGO
pygame.quit()
