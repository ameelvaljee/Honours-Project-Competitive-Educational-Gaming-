import pygame as pg
import sys
import time
from pygame.locals import *

from button import *
from settings import *
from textinputbox import *
from scoreboard import *

class start:
    def __init__(self, game):
        #window set up
        self.game = game
        self.on_screen = "start"

        #title set up
        self.game_title = pg.image.load("./resources/titles/maze_title_2.png").convert_alpha()
        self.game_title = pg.transform.scale(self.game_title, (0.4*(RES[0]), 0.4*(RES[0])*(1299/2366)))

        #button set up
        self.button_pos_x = 0.38*RES[0]
        self.button_pos_y = 0.475*RES[1]
        self.button_size_x = 0.2*(RES[0])
        self.button_size_y = 0.2*0.25*(RES[0])

        self.buttons = [
            Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Register', self.changeToReg, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 34),
            Button(self.game, self.button_pos_x, self.button_pos_y + 1*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Log-In', self.changeToLogIn, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 34),
            Button(self.game, self.button_pos_x, self.button_pos_y + 2*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Help', self.testButton, False, (255,165,0), (255,215,0), (255,140,0), 34),
            Button(self.game, self.button_pos_x, self.button_pos_y + 3*(1.2*self.button_size_y), self.button_size_x, self.button_size_y, 'Exit', self.exitgame, False, (255, 102, 102), (255, 51, 51), (76, 0, 155), 34)
        ]

        consolas_font = pg.font.SysFont(None, 30)
        self.username_input_box = TextInputBox(game, self.button_pos_x, self.button_pos_y, self.button_size_x, consolas_font, "Username Here", False, True, None)
        self.password_input_box = TextInputBox(game, self.button_pos_x, self.button_pos_y + 1*(1.1*self.button_size_y), self.button_size_x, consolas_font, "Password Here", False, True, self.username_input_box.disable)
        self.username_input_box.disable_friend = self.password_input_box.disable

        self.check_server_response = False
        self.error_text = None
        #self.scoreboard = scoreboard(self.game, [["alan_turing", 100000000], ["bane", 999], ["chad", 998], ["brad", 997], ["random_student", 50], ["calvin", 0], ["not_cs_student", -1], ["bowser", -999], ["throwing", -1000]], 6, 50, 50, 400, 300)

    def draw(self):
        #self.game.screen.fill((0, 0, 0))
        #game title
        self.game.screen.blit(self.game_title, (0.28*RES[0], 0.04*RES[1]))
        
        #start menu buttons
        for button in self.buttons:
            button.process()

        events = pg.event.get()

        #determine which screen to render
        if self.on_screen == "reg":
            self.username_input_box.update(events)
            self.password_input_box.update(events)

            if self.check_server_response:
                if self.game.receive_Q.empty():
                    pass
                else:
                    response = self.game.receive_Q.get()
                    if response.startswith("100"):
                        message_data = response.split("><")
                        username = message_data[1]
                        self.game.client_manager.change_name(username)
                        for i in range(0,3):
                            self.game.client_manager.get_updated_timeboard(i)
                            self.game.client_manager.get_updated_scoreboard(i)
                        self.game.mainmenu.scoreboard_one.update(self.game.client_manager.scoreboards[0],self.game.client_manager.scoreboard_positions[0]+1)
                        self.game.mainmenu.scoreboard_two.update(self.game.client_manager.timeboards[0],self.game.client_manager.timeboard_positions[0]+1)
                        self.game.mainmenu.updateLogIn()
                        self.game.endmenu.assign_manager(self.game.client_manager)
                        self.game.start_display = False
                        self.game.mainmenu_display = True
                        
                    else:
                        font = pg.font.SysFont(None, 30)
                        self.error_text = font.render("Username already registered", True, (255, 0, 0))
                        self.username_input_box.change_to_red()
                        self.password_input_box.change_to_red()

        elif self.on_screen == "log-in":
            self.username_input_box.update(events)
            self.password_input_box.update(events)

            if self.check_server_response:
                if self.game.receive_Q.empty():
                    pass
                else:
                    response = self.game.receive_Q.get()
                    if response.startswith("101"):
                        message_data = response.split("><")
                        username = message_data[1]
                        self.game.client_manager.change_name(username)
                        for i in range(0,3):
                            self.game.client_manager.get_updated_timeboard(i)
                            self.game.client_manager.get_updated_scoreboard(i)
                        self.game.mainmenu.scoreboard_one.update(self.game.client_manager.scoreboards[0],self.game.client_manager.scoreboard_positions[0])
                        self.game.mainmenu.scoreboard_two.update(self.game.client_manager.timeboards[0],self.game.client_manager.timeboard_positions[0])
                        if self.game.client_manager.scoreboard_positions[0] == -1:
                            self.game.mainmenu.scoreboard_one.update(self.game.client_manager.scoreboards[0], self.game.client_manager.scoreboard_positions[0])
                        else:
                            self.game.mainmenu.scoreboard_one.update(self.game.client_manager.scoreboards[0], self.game.client_manager.scoreboard_positions[0] + 1)
                        if self.game.client_manager.scoreboard_positions[0] == -1:
                            self.game.mainmenu.scoreboard_two.update(self.game.client_manager.timeboards[0], self.game.client_manager.timeboard_positions[0])
                        else:
                            self.game.mainmenu.scoreboard_two.update(self.game.client_manager.timeboards[0], self.game.client_manager.timeboard_positions[0] + 1)
                        self.game.mainmenu.updateLogIn()
                        self.game.endmenu.assign_manager(self.game.client_manager)
                        self.game.endmenu.update("score", 0)
                        self.game.start_display = False
                        self.game.mainmenu_display = True
                    elif response == "111":
                        font = pg.font.SysFont(None, 30)
                        self.error_text = font.render("Incorrect password", True, (255, 0, 0))
                        self.username_input_box.change_to_red()
                        self.password_input_box.change_to_red()
                    else:
                        font = pg.font.SysFont(None, 30)
                        self.error_text = font.render("Unrecognised username", True, (255, 0, 0))
                        self.username_input_box.change_to_red()
                        self.password_input_box.change_to_red()

        if self.error_text:
            self.game.screen.blit(self.error_text, (self.button_pos_x, (self.button_pos_y)*0.9))

        #self.scoreboard.draw()

        #pg.display.flip()
    
    def changeToReg(self):
        self.buttons = [Button(self.game, self.button_pos_x, self.button_pos_y + 2*(1.1*self.button_size_y), self.button_size_x, self.button_size_y, 'Register', self.register, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 30)]
        self.on_screen = "reg"

    def register(self):
        username = self.username_input_box.get_text()
        password = self.password_input_box.get_text()
        to_send = "{0}><{1}><{2}".format(1, username, password)
        self.game.send_Q.put(to_send)
        self.check_server_response = True

    def changeToLogIn(self):
        self.buttons = [Button(self.game, self.button_pos_x, self.button_pos_y + 2*(1.1*self.button_size_y), self.button_size_x, self.button_size_y, 'Log-In', self.log_in, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 30)]
        self.on_screen = "log-in"

    def log_in(self):
        username = self.username_input_box.get_text()
        password = self.password_input_box.get_text()
        to_send = "{0}><{1}><{2}".format(2, username, password)
        self.game.send_Q.put(to_send)
        self.check_server_response = True

    def func(self):
        self.game.to_display = "game"
        
    def testButton(self):
        self.scoreboard.update([["alan_turing", 100000000], ["calvin", 1000], ["bane", 999], ["chad", 998], ["brad", 997], ["random_student", 50], ["not_cs_student", -1], ["bowser", -999], ["throwing", -1000]], 2)
        #print("Button working")

    def exitgame(self):
        self.game.quit()