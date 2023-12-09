# 6502 Racer Game by @TokyoEdtech
# Windows, MacOSX, and Linux Compatible
# by @TokyoEdtech

import pygame
import math
import random
import os
import sys

pygame.init()
pygame.display.set_caption("6502 Racer Game by @TokyoEdtech")
clock = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create classes
class Sprite():
    def __init__(self, x, y, width, height, img = None):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.friction = 0.9
        self.heading = 0
        self.speed = 0
        self.img = img
        
        if self.img:
            self.img = pygame.image.load(os.path.join('images', img))
            self.img = pygame.transform.scale(self.img, (height, width))
            self.img.convert()
            
    def goto(self, x, y):
        self.x = x
        self.y = y

    def render(self, camera):
        if self.img:
            img = pygame.transform.rotate(self.img, -self.heading)
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(int(self.x-self.width/2.0-camera.x + WIDTH/2.0), int(self.y-self.height/2.0), self.height, self.width)) 

    def is_aabb_collision(self, other):
        # Axis Aligned Bounding Box
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)
        
    def distance(self, other):
        a = self.x - other.x
        b = self.y - other.y
        return math.sqrt(a*a + b*b)
            
class Car(Sprite):
    def __init__(self, x, y, width, height, img=None):
        Sprite.__init__(self, x, y, width, height, img)
        self.speed = 0
        self.heading = 0
        self.turn_speed = 15
        self.acceleration = 1

    def move(self):
        self.dx = self.speed * math.cos(math.radians(self.heading))
        self.dy = self.speed * math.sin(math.radians(self.heading))
                
        self.x += self.dx
        self.y += self.dy
        
    def accelerate(self):
        self.speed += self.acceleration
        
    def brake(self):
        self.speed -= self.acceleration
        
    def left(self):
        if self.speed !=0:
            self.heading -= self.turn_speed
        
    def right(self):
        if self.speed != 0:
            self.heading += self.turn_speed
            
class Player(Car):
    def __init__(self, x, y, width, height, img=None):
        Car.__init__(self, x, y, width, height, img)
        self.color = (255, 255, 0)

class sensor():
    def __init__(self, direction):
        self.direction = direction
        
    def ping(self, car, sprites):
        min_distance = 255
        
        for sprite in sprites:
            if sprite != car:
                distance = car.distance(sprite)
                if(distance < min_distance):
                    min_distance = distance 
        return min_distance

class AI_Car(Car):
    def __init__(self, x, y, width, height, img=None):
            Car.__init__(self, x, y, width, height, img)
            
            # Computer and components
            self.cpu = None
            self.memory = []
            for _ in range(65536):
                self.memory.append(0)
                
            self.sensor_distance_n = sensor(0)
    
    def poke(self, address, value):
        
        valid_address = (address >= 0) and (address <= 65535)
        valid_value = (value >= 0) and (value <= 255)
        
        if valid_address and valid_value:
            self.memory[address] = value
        else:
            print(f"Invalid: poke {address}, {value}")
    
    
    
    def tick(self, sprites):
        # Update sensor data
        
        # Distance sensors
        self.memory[16] = self.sensor_distance_n.ping(self, sprites)
        
        # Run CPU
        
        if self.memory[16] <= 50:
            self.heading -= self.turn_speed
        
        # Update car state
        # Speed
        self.speed = self.memory[1]
        
        

class Camera():
    def __init__(self, target):
        self.x = target.x
        self.y = target.y
        
    def update(self, target):
        # self.x = target.x
        # self.y = target.y
        self.x = 0
        self.y = 0

# Create font

# Create sounds

# Create game objects
player = Player(600, 300, 15, 30, "car_yellow.png")

ai_cars = []

ai_car = AI_Car(300, 300, 15, 30, "car_blue.png")
ai_car.poke(1, 1) # Set speed to 1

ai_cars.append(ai_car)

ai_car = AI_Car(900, 300, 15, 30, "car_lime.png")

ai_cars.append(ai_car)

# Create camera object
camera = Camera(player)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.accelerate()
            elif event.key == pygame.K_DOWN:
                player.brake()

    # Move/Update objects
    player.move()
    
    for ai_car in ai_cars:
        temp = ai_cars[:]
        temp.append(player)
        ai_car.tick(temp)
        ai_car.move()
        
    # camera.update(player)
        
    # Render (Draw stuff)
    # Fill the background color
    screen.fill(BLACK)
    
    # Render objects
    player.render(camera)
    
    for ai_car in ai_cars:
        ai_car.render(camera)
     
    # Flip the display
    pygame.display.flip()
    
    # Set the FPS
    clock.tick(30)
