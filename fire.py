import pygame as pg 
import time
import sys
from settings import *
from pygame import gfxdraw
from random import randint

STEPS_BETWEEN_COLORS = 9
COLORS = ['black', 'red', 'orange', 'yellow', 'white']
PIXEL_SIZE = 4

FIRE_REPS = 4
FIRE_WIDTH = WIDTH // (PIXEL_SIZE)# * FIRE_REPS)
FIRE_HEIGHT = HEIGHT // PIXEL_SIZE 


'''*****************************************************
Class: Fire --> Creats fire annimation for game startup 

Acknowledgement: Stanislav Petrov        
https://github.com/StanislavPetrovV/DOOM-Fire-Algorithm

********************************************************'''
class Fire:

    def __init__(self,game):
        self.game = game
        self.palette = self.get_palette()
        self.firearray = self.getfirearray()
        self.firesurface = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])

    def getfirearray(self):
        firearray = [[0 for i in range (FIRE_WIDTH)] for j in range (FIRE_HEIGHT)]
        for i in range (FIRE_WIDTH):
            firearray [ FIRE_HEIGHT -1][i] = len(self.palette) -1
        return firearray

    def drawfire(self):
        for y, row in enumerate(self.firearray):
            for x, colour_index in enumerate(row):
                if colour_index:
                    colour = self.palette[colour_index]
                    gfxdraw.box(self.game.screen, (x*PIXEL_SIZE, (y)*PIXEL_SIZE, PIXEL_SIZE-1,PIXEL_SIZE-1 ), colour) #y-110
                    

    def makefire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1,FIRE_HEIGHT):
                colour_index = self.firearray[y][x]
                if colour_index:
                    randomnum = randint(0,3)
                    self.firearray[y-1][(x - randomnum + 1)% FIRE_WIDTH] = colour_index -randomnum%2
                else:
                    self.firearray[y-1][x] = 0

    def update(self):
        self.makefire()

    def draw(self):
        self.drawfire()

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pg.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette