import random
import pygame
import time
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVIDADE = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
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
        self.image = self.images[self.current_image]

        self.speed += GRAVIDADE

        # altura
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

def display_text(text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def display_game_over():
    game_over_font = pygame.font.Font(None, 80)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(game_over_text, game_over_rect)

def display_start_screen():
    start_font = pygame.font.Font(None, 80)
    start_text = start_font.render("Flappy Bird", True, (255, 255, 255))
    start_rect = start_text.get_rect()
    start_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(start_text, start_rect)

    start_instructions_font = pygame.font.Font(None, 30)
    start_instructions_text = start_instructions_font.render("Press SPACE to start", True, (0, 0, 0))
    start_instructions_rect = start_instructions_text.get_rect()
    start_instructions_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    screen.blit(start_instructions_text, start_instructions_rect)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

BACKGROUND = pygame.image.load('bg.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

score = 0
last_pipe = None
game_over = False
start_screen = True

while True:
    while start_screen:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    start_screen = False

        screen.blit(BACKGROUND, (0, 0))
        display_start_screen()
        pygame.display.update()

    while not game_over:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or \
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask):
            game_over = True

        incremento = 0
        for pipe in pipe_group:
            if pipe.rect[0] < bird.rect[0] and not pipe.passed:
                score += incremento
                incremento = 1
                pipe.passed = True

        display_text(str(score), 50, SCREEN_WIDTH // 2, 50, (255, 255, 255))

        if game_over:
            display_game_over()
            pygame.display.update()

            while game_over:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            score = 0
                            bird.rect[0] = SCREEN_WIDTH / 2
                            bird.rect[1] = SCREEN_HEIGHT / 2
                            bird.speed = SPEED
                            bird_group.empty()
                            bird_group.add(bird)
                            pipe_group.empty()
                            ground_group.empty()
                            for i in range(2):
                                ground = Ground(GROUND_WIDTH * i)
                                ground_group.add(ground)
                            for i in range(2):
                                pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
                                pipe_group.add(pipes[0])
                                pipe_group.add(pipes[1])
                            game_over = False

        pygame.display.update()
