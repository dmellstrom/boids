#!/usr/bin/env python

'''
    simulation.py

    simulation.py runs a simple particle simulation in which the boids are
    drawn together by flocking behavior. Utilizes boid.py and the pygame
    library available at pygame.org.
'''

import pygame
from pygame.locals import *
from boid import *
from random import *
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
BG_COLOR = [0, 0, 0]
BOID_FILENAMES = [
    'bat1.bmp',
    'bat2.bmp',
    'bat3.bmp',
    'bat4.bmp']
ECCENTRICITY = 100.0
FRIENDLINESS = 30.0
CONFORMITY = 10.0
STAY_ON_SCREEN = True

pygame.init()
screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

frames = []
for filename in BOID_FILENAMES:
    frame = pygame.image.load(filename)
    frames.append(frame)

boids = []

print "Press the spacebar to ready the simulation, and again to start it. Click to place boids."

#for i in range(NUM_BOIDS):
#    boids.append(Boid(frames, 150, 20.0, ECCENTRICITY, FRIENDLINESS, CONFORMITY, random() * SCREEN_WIDTH, random() * SCREEN_HEIGHT, (random() * 20) - 10, (random() * 20) - 10))

waiting = True

while waiting:
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            _ = pygame.key.name(e.key)
            if _ == "space":
                waiting = False
    screen.fill([255, 255, 255])
    time_passed = clock.tick(60)

cooldown = -1

waiting = True

while True:
    time_passed = clock.tick(60)
    screen.fill(BG_COLOR)
    time = pygame.time.get_ticks()

    if cooldown > -1:
        cooldown -= 1

    for e in pygame.event.get():
        if e.type == MOUSEBUTTONDOWN:
            if cooldown < 0:
                boids.append(Boid(frames, 150, 20.0, ECCENTRICITY, FRIENDLINESS, CONFORMITY, e.pos[0], e.pos[1], (random() * 20) - 10, (random() * 20) - 10))
                cooldown = 59
        if e.type == KEYDOWN:
            _ = pygame.key.name(e.key)
            if _ == "space":
                waiting = False
        if e.type == QUIT:
            exit()
    if not waiting:
        for boid in boids:
            boid.update(boids)
            if STAY_ON_SCREEN:
                if boid.x > SCREEN_WIDTH or boid.x < 0:
                    if boid.x > SCREEN_WIDTH:
                        boid.x = SCREEN_WIDTH - 1
                    if boid.x < 0:
                        boid.x = 0
                    for eachBoid in boids:
                        eachBoid.vx = -eachBoid.vx
                if boid.y > SCREEN_HEIGHT or boid.y < 0:
                    if boid.y > SCREEN_HEIGHT:
                        boid.y = SCREEN_HEIGHT - 1
                    if boid.y < 0:
                        boid.y = 0
                    for eachBoid in boids:
                        eachBoid.vy = -eachBoid.vy
    for boid in boids:
        rotatedImage = pygame.transform.rotate(boid.image, -(math.degrees(boid.dir) + 180))
        screen.blit(rotatedImage, boid.rect)

    pygame.display.update()
