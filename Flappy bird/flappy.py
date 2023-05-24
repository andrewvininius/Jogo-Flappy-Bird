import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVIDADE = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGT = 100

PIPE_WIDTH = 120
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bird1.png').convert_alpha(),
                       pygame.image.load('bird2.png').convert_alpha(),
                       pygame.image.load('bird3.png').convert_alpha()]
        
        self.speed = SPEED
        
        self.current_image = 0

        self.image = pygame.image.load('bird2.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3 
        self.image = self.images[self.current_image ]

        self.speed += GRAVIDADE

        # altura
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self,inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:  
            self.rect[1] = SCREEN_HEIGHT - ysize  
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect[0] -= GAME_SPEED
        

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGT))

        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect [0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100,300)
    pipe = Pipe(False,xpos,size)
    pipe_inverted = Pipe(True,xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) 

BACKGROUND = pygame.image.load('bg.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH,SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird) 

ground_group = pygame.sprite.Group()
for i in range (2):
    ground = Ground(GROUND_WIDTH * i )
    ground_group.add(ground)

pipe_group  = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group .add(pipes[0])
    pipe_group .add(pipes[1])
    
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event. type == QUIT:
           pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND,(0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    bird_group.update()
    ground_group.update()
    pipe_group .update()
    
    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group .draw(screen)

    pygame.display.update() 

    if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask):
        #Game Over
        pygame.display.update()
        input()
        break     





