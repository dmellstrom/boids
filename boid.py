'''
    boid.py

    Objects of the Boid class represent particles which exhibit a customizable
    inclination to flock together. Depends on pygame, available at pygame.org.
'''

import pygame
import math
from random import *

class Boid(pygame.sprite.Sprite):
    def __init__(self, images, delay, mass, eccentricity, friendliness, conformity, x, y, vx, vy):
        self._delay = delay
        self._last_update = 0
        self._frame = 0
        self._images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mass = mass
        self.eccentricity = eccentricity
        self.friendliness = friendliness
        self.conformity = conformity
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dir = 0.0

    def distanceTo(self, otherBoid):
        return math.sqrt(math.pow((self.x - otherBoid.x), 2) + math.pow((self.y - otherBoid.y), 2))

    def randSignedRepel(self):
        return 25.0 * float((randint(0,1) * 2) - 1)

    def updateDir(self):
        if self.vx == 0:
            if self.vy > 0:
                self.dir = math.pi
            elif self.vy < 0:
                self.dir = 0.0
        elif self.vy == 0:
            if self.vx > 0:
                self.dir = (3 * math.pi) / 4
            elif self.vx < 0:
                self.dir = math.pi / 4
        else:
            self.dir = math.atan(self.vx / -self.vy)

        if self.vy < 0:
            if dir < 0:
                self.dir += math.pi
            else:
                self.dir -= math.pi

    def update(self, boidList):
        ticks = pygame.time.get_ticks() - self._last_update
        #change frame of animated sprite
        if ticks > self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
                self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = pygame.time.get_ticks()
        
        dt = (float(ticks) / 1000)
        
        # modify boid's velocity based on knowledge of the environment
        xForce = 0.0
        yForce = 0.0
        for boid in boidList:
            if boid != self:
                distance = self.distanceTo(boid)
                #repel from neighbors if too close
                if distance < 15.0:
                    repelForce = self.mass * 50.0
                    xRepelForce = self.randSignedRepel() if distance == 0.0 else ((self.x - boid.x) / distance) * repelForce
                    xForce += xRepelForce
                    yRepelForce = self.randSignedRepel() if distance == 0.0 else ((self.y - boid.y) / distance) * repelForce
                    yForce += yRepelForce
                #approach neighbors
                approachForce = self.mass * (self.friendliness / 10.0)
                xApproachForce = 0.0 if distance == 0.0 else ((boid.x - self.x) / distance) * approachForce
                xForce += xApproachForce
                yApproachForce = 0.0 if distance == 0.0 else ((boid.y - self.y) / distance) * approachForce
                yForce += yApproachForce
                #match velocity of close neighbors
                if distance < 15.0:
                    self.vx += (boid.vx - self.vx) * (self.conformity / 100.0)
                    self.vy += (boid.vy - self.vy) * (self.conformity / 100.0)
        #physics...
        ax = xForce / self.mass
        ay = yForce / self.mass
        self.vx += ax * dt
        self.vy += ay * dt
        # regulate velocity
        velocity = math.sqrt(math.pow(self.vx, 2) + math.pow(self.vy, 2))
        self.updateDir()
        direction = self.dir
        # add random fluctuations
        fluctuation = (self.eccentricity / 100.0) * (((random() * math.pi) / 25.0) - (math.pi / 50.0))
        direction += fluctuation
        self.vx = -math.sin(direction) * velocity
        self.vy = math.cos(direction) * velocity
        if velocity > 30.0:
            self.vx = (self.vx / velocity) * 30
            self.vy = (self.vy /velocity) * 30
        if velocity < 15.0:
            self.vy = self.vy * 1.1
            self.vx = self.vx * 1.1
        #update position & direction
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (self.x, self.y)
