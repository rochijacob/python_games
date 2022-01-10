import pygame
from pygame.locals import *

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

#load images
bg = pygame.image.load('assets/bg.png')
ground_img = pygame.image.load('assets/ground.png')


#Main Game Loop
run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (-100,-200))

    #draw and scroll ground
    screen.blit(ground_img, (ground_scroll, screen_height - 150))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    #get all events happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()