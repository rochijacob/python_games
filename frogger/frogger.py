#Topics: Classes, inheritance, Turtle Graphics 
import turtle
import math
import time
import random

wn = turtle.Screen()
wn.cv._rootwindow.resizable(False, False)
wn.title('Frogger')
wn.setup(600, 800)
wn.bgcolor('black')
wn.tracer(0)

#register shape
wn.register_shape("assets/frog.gif")
wn.register_shape("assets/car_left.gif")
wn.register_shape("assets/car_right.gif")
wn.register_shape("assets/log_full.gif")



pen= turtle.Turtle()
pen.speed(0)
pen.hideturtle()

#Create classes
class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_collision(self, other):
        #Axis align bounding box - Tells us if two objects collide
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)


#parent is a child of Sprite class
class Player(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0

    def up(self):
        self.y += 50

    def down(self):
        self.y -= 50

    def right(self):
        self.x += 50

    def left(self):
        self.x -= 50

    def update(self):
        self.x += player.dx
    
    #Border Checking
        if self.x < -300 or self.x > 300:
            self.x = 0
            self.y = -300

class Car(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
    #update function
    def update(self):
        self.x += self.dx

        #Border Checking
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

class Log(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
    #update function
    def update(self):
        self.x += self.dx

        #Border Checking
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

#Create objects
player = Player(0, -300, 40, 40, 'assets/frog.gif')
player.render(pen)

car_left = Car(0, -250, 121, 40, "assets/car_left.gif", -0.04)
car_right = Car(0, -200, 121, 40, "assets/car_right.gif", 0.04)
log_right = Log(0, -150, 121, 40, "assets/log_full.gif", 0.06)
log_left = Log(0, -100, 121, 40, "assets/log_full.gif", -0.06)

#Create list of sprites
sprites = [ car_left, car_right, log_right, log_left, player]
sprites.append(player)

#keyboard binding
wn.listen()
wn.onkeypress(player.up, 'Up')
wn.onkeypress(player.down, 'Down')
wn.onkeypress(player.right, 'Right')
wn.onkeypress(player.left, 'Left')


while True:

    #update the objects
    for sprite in sprites:
        sprite.render(pen)
        sprite.update()

    #Check for collisions
    player.dx = 0
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):
                player.x = 0
                player.y = -300
                break
            elif isinstance(sprite, Log):
                player.dx = sprite.dx
                break

    #update screen
    wn.update()

    #clear the pen
    pen.clear()


