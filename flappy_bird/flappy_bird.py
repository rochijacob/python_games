import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

#Game Window
screen_width = 664
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

#load images
bg = pygame.image.load('assets/bg.png')
ground_img = pygame.image.load('assets/ground.png')

#Bird Sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index  = 0
        self.counter = 0 #animation speed
        for num in range(1, 4):
            img = pygame.image.load(f'assets/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):

        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height - 150:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 15

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

#Pipes Sprites
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap /2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap /2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height /2))

bird_group.add(flappy)

#Main Game Loop
run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (-100,-200))

    #bird group
    bird_group.draw(screen)
    bird_group.update()

    #pipe group
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, screen_height - 150))

    #check for colision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #check collision with ground
    if flappy.rect.bottom > screen_height - 150:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width,  int(screen_height /2) + pipe_height, -1)
            top_pipe = Pipe(screen_width,  int(screen_height /2) + pipe_height, 1)
            pipe_group.add(btm_pipe, top_pipe)

            last_pipe = time_now


        #draw and scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()
        

    #get all events happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()