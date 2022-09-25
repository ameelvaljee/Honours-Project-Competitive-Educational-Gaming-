import pygame as pg 
import sys

from button import *
from settings import *
from textinputbox import *
from scoreboard import *
from timer import *
from timeboard import *

class mainmenu:
    def __init__(self, game):
        #window set up
        self.game = game

        #title set up
        self.game_title = pg.image.load("./resources/titles/maze_title_2.png").convert_alpha()
        self.game_title = pg.transform.scale(self.game_title, (0.3*(RES[0]), 0.3*(RES[0])*(1299/2366)))

        #button set up
        self.button_pos_x = 0.2*RES[0]
        self.button_pos_y = 0.4*RES[1]
        self.button_size_x = 0.2*(RES[0])
        self.button_size_y = 0.2*0.25*(RES[0])

        #self.timer = timer(game, 0, 0, 120, True)

        self.timeboard_index = 0
        self.scoreboard_index = 0

        self.buttons = [
            Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Play Tutorial', self.tutorialButton, False, (204, 102, 255), (255, 0, 255), (102, 0, 102), 25),
            Button(self.game, self.button_pos_x, self.button_pos_y + 1*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Play Point Mode', self.pointButton, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 25),
            Button(self.game, self.button_pos_x, self.button_pos_y + 2*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Play Time Mode', self.timeButton, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 25),
            Button(self.game, self.button_pos_x, self.button_pos_y + 3*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Help', self.helpButton, False, (255,165,0), (255,215,0), (255,140,0), 25),
            Button(self.game, self.button_pos_x, self.button_pos_y + 4*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Exit', self.exitgame, False, (255, 102, 102), (255, 51, 51), (76, 0, 155), 25),
            Button(self.game, 800, 350, 200, 50, '<<', self.prevScoreBoard, False, (255,165,0), (255,215,0), (255,140,0), 50),
            Button(self.game, 1000, 350, 200, 50, '>>', self.nextScoreBoard, False, (255,165,0), (255,215,0), (255,140,0), 50),
            Button(self.game, 800, 750, 200, 50, '<<', self.prevTimeBoard, False, (255,165,0), (255,215,0), (255,140,0), 50),
            Button(self.game, 1000, 750, 200, 50, '>>', self.nextTimeBoard, False, (255,165,0), (255,215,0), (255,140,0), 50)
        ]

        self.scoreboard_one = scoreboard(self.game, "Score Mode Map 1", [["alan_turing", 100000000], ["bane", 999], ["chad", 998], ["brad", 997], ["random_student", 50], ["calvin", 0], ["not_cs_student", -1], ["bowser", -999], ["throwing", -1000]], -1, 800, 50, w = 400, h = 300)
        self.scoreboard_two = timeboard(self.game, "Time Mode Map 1", [["alan_turing", 100000000], ["calvin", 1000], ["bane", 999], ["chad", 998], ["brad", 997], ["random_student", 50], ["not_cs_student", -1], ["bowser", -999], ["throwing", -1000]], -1, 800, 450, w = 400, h = 300)

        self.font = pg.font.SysFont(None, 30)
        self.logged_in_text = self.font.render("Logged in as: {0}".format(self.game.client_manager.name), True, (255, 255, 255))

        

    def draw(self):
        """Draws and displays the screen for the game objects"""
        self.game.screen.fill((0, 0, 0))
        #game title
        self.game.screen.blit(self.game_title, (0.15*RES[0], 0.125*RES[1]))
        
        #start menu buttons
        for button in self.buttons:
            button.process()

        self.scoreboard_one.draw()
        self.scoreboard_two.draw()

        self.game.screen.blit(self.logged_in_text, (0.425*RES[0], 0.96*RES[1]))

        #self.timer.draw()

    def updateLogIn(self):
        """Update 'logged in as' text"""
        self.logged_in_text = self.font.render("Logged in as: {0}".format(self.game.client_manager.name), True, (255, 255, 255))

    def helpButton(self):
        """Makes a call to the help UI to display"""
        self.game.helpbutton()

    def testButton(self):
        print("Button is working")

    def tutorialButton(self):
        """Start the user tutorial and display elements"""
        self.game.tutorialmode = True
        self.game.new_game('tutorial')
        self.game.editor_display = True
        self.game.mapdisplay = True

        self.game.mainmenu_display = False

    def pointButton(self):
        """Start a point game and display elements"""
        self.game.pointg1 = True
        self.game.new_game('pointg1')
        self.game.editor_display = True
        self.game.mapdisplay = True

        self.game.mainmenu_display = False

    def timeButton(self):
        """Start a time game and display elements"""    
        self.game.timeg1 = True
        self.game.new_game('timeg1', pos = (1.5, 5.5),time = 300)
        self.game.timer.resume()
        self.game.editor_display = True
        self.game.mapdisplay = True

        self.game.mainmenu_display = False

    def exitgame(self):
        """Makes a call to exit the entire program"""
        self.game.quit()

    def prevTimeBoard(self):
        """Traverse leaderboards UI to the previous time leaderboard"""
        if self.timeboard_index == 0:
            pass
        else:
            self.timeboard_index = self.timeboard_index - 1
            self.scoreboard_two.updateTitle("Time Mode Map {0}".format(self.timeboard_index+1))
            self.scoreboard_two.update(self.game.client_manager.timeboards[self.timeboard_index], self.game.client_manager.timeboard_positions[self.timeboard_index]+1)

    def nextTimeBoard(self):
        """Traverse leaderboards UI to the next time leaderboard"""
        if self.timeboard_index == 2:
            pass
        else:
            self.timeboard_index = self.timeboard_index + 1
            self.scoreboard_two.updateTitle("Time Mode Map {0}".format(self.timeboard_index+1))
            self.scoreboard_two.update(self.game.client_manager.timeboards[self.timeboard_index], self.game.client_manager.timeboard_positions[self.timeboard_index]+1)

    def prevScoreBoard(self):
        """Traverse leaderboards UI to the previous score leaderboard"""
        if self.scoreboard_index == 0:
            pass
        else:
            self.scoreboard_index = self.scoreboard_index - 1
            self.scoreboard_one.updateTitle("Score Mode Map {0}".format(self.scoreboard_index+1))
            self.scoreboard_one.update(self.game.client_manager.scoreboards[self.scoreboard_index], self.game.client_manager.scoreboard_positions[self.scoreboard_index]+1)

    def nextScoreBoard(self):
        """Traverse leaderboards UI to the next score leaderboard"""
        if self.scoreboard_index == 2:
            pass
        else:
            self.scoreboard_index = self.scoreboard_index + 1
            self.scoreboard_one.updateTitle("Score Mode Map {0}".format(self.scoreboard_index+1))
            self.scoreboard_one.update(self.game.client_manager.scoreboards[self.scoreboard_index], self.game.client_manager.scoreboard_positions[self.scoreboard_index]+1)