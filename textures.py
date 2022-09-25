import pygame as pg
from settings import * 
import sys

class Textures:

    def __init__(self, game):
        self.game = game 
        self.screen = game.screen 
        self.wall_textures = self.load_wall_textures() 
        self.skyimage = pg.image.load('resources/wall/sky.png')
        self.bloodtex = pg.image.load('resources/blood_screen.png')
        
        self.skyoffset = 0
        self.skyimage = pg.transform.scale(self.skyimage,(WIDTH,HALF_HEIGHT))
        self.font = pg.font.Font('resources/text.ttf', 20)

    def drawsky(self):
        '''**********************************************

        Method: drawsky --> Draws the seemless sky image


        **************************************************'''
        self.skyoffset = (45*-self.game.player.angle)%WIDTH
        #print(self.skyoffset)
        #print(self.game.player.angle)
        self.screen.blit(self.skyimage, (-self.skyoffset, 0))
        self.screen.blit(self.skyimage, (-self.skyoffset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
          


    def render_textures(self): 
        '''*****************************************************************************************************

        Method: render_textures --> performs all required rendering
        
        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ********************************************************************************************************'''
        stuff_to_render = sorted(self.game.raycast.items_render,key=lambda t:t[0],reverse=True)
        for depth,column,pos in (stuff_to_render):
            self.screen.blit(column,pos)

    def get_texture(path,res):
        '''*****************************************************************************************************

        Method: get_texture --> loads and scales the wall img

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ********************************************************************************************************'''
        texture = pg.image.load('resources/wall/1.png').convert_alpha()

        res=(TEXTURE_SIZE, TEXTURE_SIZE)

        return pg.transform.scale(texture, res)

   
    def load_wall_textures(self):
        '''*****************************************************************************************************

        Method: get_texture --> allows the developer to load multiple styles of walls

        ********************************************************************************************************'''
        return {
            1: self.get_texture('resources/wall/1.png'),
            2: self.get_texture('resources/wall/2.png'),
        } 

    def bloodscreen(self):
        '''**********************************************

        Method: drawsky --> Draws a semi transparent red screen 
                            when player takes damage

        **************************************************'''
        self.screen.blit(self.bloodtex, (0,0)) 

    def pointsgame(self):
        '''**********************************************

        Method: pointsgame --> Displays attempts remaining

        **************************************************'''
        txt = 'ATTEMPTS REMAINING: ' + str(self.game.player.attempts)
        textsurface = self.font.render(txt, True, (200, 200, 200))
        self.screen.blit(textsurface,(10, HALF_HEIGHT+150))

    def tutorial2(self):
        '''**********************************************

        Method: tutorial2 --> Draws the tutorial instructions
        
        **************************************************'''
        self.tut1 = pg.transform.scale(self.game.player.tutimg,(800,500))
        self.screen.blit(self.tut1, (300,0))              
    def draw(self):
        self.drawsky()
        self.render_textures()
        if self.game.tutorialmode:
            self.tutorial2()
        if self.game.pointg1 or self.game.pointg2 or self.game.pointg3:
            self.pointsgame()